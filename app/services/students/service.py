"""Service métier du profil élève.

**Responsabilités** :
- Résoudre ``level_name`` + ``cycle`` → ``Level`` (UUID).
- Résoudre ``series_code`` + ``cycle`` → ``Series`` (UUID).
- Valider la compatibilité niveau ↔ série via ``level_series``.
- Mettre à jour (upsert) ``StudentProfile``.
- Construire la réponse avec entités imbriquées.

**Cache** : les options d'onboarding sont cachées 1h (elles ne changent quasi
jamais). Le profil lui-même n'est pas caché (personnel, évolue souvent).
"""
from __future__ import annotations

import secrets
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logging import log as logger
from app.db.redis import get_redis
from app.models import (
    Cycle,
    Level,
    LevelSeries,
    ParentStudent,
    Series,
    StudentProfile,
    User,
    UserRole,
)
from app.schemas.referential import LevelRead, SeriesRead
from app.schemas.students import (
    CycleOptions,
    LevelWithSeries,
    StudentProfilePublic,
    StudentProfileRead,
    StudentProfileUpsertRequest,
)
from app.services.cache import ReferentialCache
from app.services.students.errors import (
    LevelNotFoundError,
    NotAStudentError,
    NotGuardianError,
    ProfileNotFoundError,
    SeriesNotAllowedForLevelError,
    SeriesNotFoundError,
    StudentError,
)

PROFILE_OPTIONS_TTL = 3600
PAIRING_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # pas de 0/O/1/I


class StudentsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ==================================================================
    # Upsert profil
    # ==================================================================

    async def upsert_profile(
        self,
        *,
        user: User,
        payload: StudentProfileUpsertRequest,
    ) -> StudentProfileRead:
        """Crée ou met à jour le profil élève.

        Étapes :
        1. Vérifier que l'utilisateur est bien un élève.
        2. Résoudre le niveau (name + cycle).
        3. Résoudre la série (code + cycle) si fournie.
        4. Vérifier que la série est autorisée pour ce niveau.
        5. Mettre à jour ``StudentProfile``.
        """
        if user.role is not UserRole.STUDENT:
            raise NotAStudentError()

        # 1. Résoudre le niveau
        level = await self.session.scalar(
            select(Level).where(
                Level.name == payload.level_name,
                Level.cycle == payload.cycle,
            )
        )
        if level is None:
            raise LevelNotFoundError(
                payload.level_name, payload.cycle.value
            )

        # 2. Résoudre la série (si fournie)
        series: Series | None = None
        if payload.series_code:
            series = await self.session.scalar(
                select(Series).where(
                    Series.code == payload.series_code,
                    Series.cycle == payload.cycle,
                )
            )
            if series is None:
                raise SeriesNotFoundError(
                    payload.series_code, payload.cycle.value
                )

            # 3. Vérifier que la série est autorisée pour ce niveau
            link = await self.session.scalar(
                select(LevelSeries).where(
                    LevelSeries.level_id == level.id,
                    LevelSeries.series_id == series.id,
                )
            )
            if link is None:
                raise SeriesNotAllowedForLevelError(
                    payload.series_code, payload.level_name
                )

        # 4. Récupérer (ou créer) le profil
        profile = await self.session.get(StudentProfile, user.id)
        if profile is None:
            # Cas défensif : register aurait dû créer le profil
            logger.warning(
                "StudentProfile manquant pour user=%s, création à la volée",
                user.id,
            )
            profile = StudentProfile(
                user_id=user.id,
                pairing_code=self._generate_pairing_code(),
            )
            self.session.add(profile)

        profile.level_id = level.id
        profile.series_id = series.id if series else None

        await self.session.flush()
        await self.session.commit()

        # Recharger avec relations pour la réponse
        await self.session.refresh(profile, attribute_names=["level", "series"])
        return self._to_read(profile)

    # ==================================================================
    # Lecture profil (self)
    # ==================================================================

    async def get_my_profile(self, *, user: User) -> StudentProfileRead:
        if user.role is not UserRole.STUDENT:
            raise NotAStudentError()
        return await self._get_profile_or_raise(user.id)

    # ==================================================================
    # Lecture profil (par un parent)
    # ==================================================================

    async def get_profile_for_guardian(
        self, *, guardian: User, student_id: UUID
    ) -> StudentProfilePublic:
        """Lecture d'un profil enfant par un parent.

        Vérifie le lien ``parent_student``. Renvoie 403 si le lien n'existe
        pas (au lieu d'un 404, pour ne pas révéler l'existence du compte).
        """
        if guardian.role is not UserRole.PARENT:
            raise NotGuardianError()

        link = await self.session.scalar(
            select(ParentStudent).where(
                ParentStudent.parent_id == guardian.id,
                ParentStudent.student_id == student_id,
            )
        )
        if link is None:
            raise NotGuardianError()

        # Récupérer le profil + user
        profile = await self.session.get(
            StudentProfile,
            student_id,
            options=[
                selectinload(StudentProfile.level),
                selectinload(StudentProfile.series),
                selectinload(StudentProfile.user),
            ],
        )
        if profile is None:
            raise ProfileNotFoundError()

        return StudentProfilePublic(
            user_id=profile.user_id,
            first_name=profile.user.first_name,
            last_name=profile.user.last_name,
            level=LevelRead.model_validate(profile.level) if profile.level else None,
            series=SeriesRead.model_validate(profile.series) if profile.series else None,
            xp_points=profile.xp_points,
            current_streak=profile.current_streak,
            longest_streak=profile.longest_streak,
        )

    # ==================================================================
    # Options d'onboarding (caché)
    # ==================================================================

    async def get_profile_options(self) -> list[CycleOptions]:
        """Retourne tous les cycles avec leurs niveaux et séries.

        Caché 1h dans Redis (clé versionnée ``ref:profile_options``).
        """
        redis = await get_redis()
        cache = ReferentialCache(redis)
        filters: dict[str, Any] = {"scope": "all"}

        cached = await cache.get("profile_options", filters)
        if cached:
            return [CycleOptions.model_validate(c) for c in cached["cycles"]]

        # Requête : tous les niveaux + leurs séries autorisées
        levels = (
            await self.session.execute(
                select(Level).order_by(Level.order_index, Level.name)
            )
        ).scalars().all()

        # Précharger les associations level_series + series
        associations = (
            await self.session.execute(
                select(LevelSeries, Series)
                .join(Series, Series.id == LevelSeries.series_id)
                .order_by(Series.code)
            )
        ).all()
        series_by_level: dict[UUID, list[Series]] = {}
        for assoc, series in associations:
            series_by_level.setdefault(assoc.level_id, []).append(series)

        # Regrouper par cycle
        by_cycle: dict[Cycle, list[LevelWithSeries]] = {}
        for lvl in levels:
            by_cycle.setdefault(lvl.cycle, []).append(
                LevelWithSeries(
                    level=LevelRead.model_validate(lvl),
                    series=[
                        SeriesRead.model_validate(s)
                        for s in series_by_level.get(lvl.id, [])
                    ],
                )
            )

        result = [
            CycleOptions(cycle=cycle, levels=items)
            for cycle, items in by_cycle.items()
        ]

        # Cache
        await cache.set(
            "profile_options",
            filters,
            {"cycles": [c.model_dump(mode="json") for c in result]},
            ttl=PROFILE_OPTIONS_TTL,
        )
        return result

    # ==================================================================
    # Régénération du pairing_code
    # ==================================================================

    async def regenerate_pairing_code(self, *, user: User) -> str:
        """Génère un nouveau code parent (invalide l'ancien).

        À utiliser si le code est compromis (partagé par erreur).
        """
        if user.role is not UserRole.STUDENT:
            raise NotAStudentError()

        profile = await self.session.get(StudentProfile, user.id)
        if profile is None:
            raise ProfileNotFoundError()

        # Boucle anti-collision (très improbable en pratique)
        for _ in range(5):
            new_code = self._generate_pairing_code()
            exists = await self.session.scalar(
                select(StudentProfile).where(
                    StudentProfile.pairing_code == new_code,
                    StudentProfile.user_id != user.id,
                )
            )
            if exists is None:
                break
        else:
            raise StudentError(
                "Impossible de générer un code unique, réessaie.",
                status_code=500,
            )

        profile.pairing_code = new_code
        await self.session.flush()
        await self.session.commit()
        return new_code

    # ==================================================================
    # Helpers
    # ==================================================================

    async def _get_profile_or_raise(self, user_id: UUID) -> StudentProfileRead:
        profile = await self.session.get(
            StudentProfile,
            user_id,
            options=[
                selectinload(StudentProfile.level),
                selectinload(StudentProfile.series),
            ],
        )
        if profile is None:
            raise ProfileNotFoundError()
        return self._to_read(profile)

    def _to_read(self, profile: StudentProfile) -> StudentProfileRead:
        return StudentProfileRead(
            user_id=profile.user_id,
            level=LevelRead.model_validate(profile.level) if profile.level else None,
            series=SeriesRead.model_validate(profile.series) if profile.series else None,
            xp_points=profile.xp_points,
            current_streak=profile.current_streak,
            longest_streak=profile.longest_streak,
            last_streak_date=profile.last_streak_date,
            pairing_code=profile.pairing_code,
        )

    @staticmethod
    def _generate_pairing_code() -> str:
        """Génère un code à 6 caractères non ambigu (pas de 0/O/1/I)."""
        return "".join(
            secrets.choice(PAIRING_CODE_ALPHABET) for _ in range(6)
        )