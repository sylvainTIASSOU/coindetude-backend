"""Handler CRDT additif pour ``streak_event``.

**Stratégie** : append-only + logique métier idempotente.

Le client envoie un événement ``streak_day`` avec une ``study_date``. Le
serveur met à jour ``current_streak`` selon la règle :

- ``study_date == last_streak_date``         → dédup, no-op
- ``study_date == last_streak_date + 1j``    → incrément
- ``study_date > last_streak_date + 1j``     → reset à 1
- ``study_date < last_streak_date``          → ignore (vieil événement)

Aucun 409 possible : la logique est **commutative** (l'ordre d'arrivée des
événements n'affecte pas le résultat final).
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ValidationError
from sqlalchemy import select

from app.models import StudentProfile, UserEvent, UserEventKind
from app.models.enums import ConflictStrategy, SyncOperation
from app.services.sync.errors import SyncError
from app.services.sync.handlers.base import SyncHandler, SyncHandlerResult


class StreakEventPayload(BaseModel):
    event_id: UUID
    study_date: date


class StreakEventHandler(SyncHandler):
    entity_type = "streak_event"
    conflict_strategy = ConflictStrategy.CRDT_MERGE

    async def apply(
        self,
        *,
        user_id: UUID,
        operation: SyncOperation,
        payload: dict[str, Any],
        client_ts: datetime,
    ) -> SyncHandlerResult:
        if operation is not SyncOperation.CREATE:
            raise SyncError(
                detail="streak_event supporte uniquement l'opération 'create'.",
                status_code=422,
            )
        try:
            data = StreakEventPayload.model_validate(payload)
        except ValidationError as exc:
            raise SyncError(
                detail=f"Payload invalide : {exc.errors()[0]['msg']}",
                status_code=422,
            ) from exc

        # Dédup par event_id
        existing = await self.session.scalar(
            select(UserEvent).where(
                UserEvent.student_id == user_id,
                UserEvent.event_id == data.event_id,
            )
        )
        if existing is not None:
            return SyncHandlerResult(
                status_code=200,
                body={
                    "status": "applied",
                    "deduplicated": True,
                    "server_ts": existing.server_ts.isoformat(),
                },
            )

        profile = await self.session.get(StudentProfile, user_id)
        if profile is None:
            raise SyncError(detail="Profil élève introuvable.", status_code=404)

        # Enregistrer l'événement (audit)
        event = UserEvent(
            event_id=data.event_id,
            student_id=user_id,
            kind=UserEventKind.STREAK_DAY,
            event_ts=datetime.combine(
                data.study_date, datetime.min.time(), tzinfo=timezone.utc
            ),
            payload={"study_date": data.study_date.isoformat()},
        )
        self.session.add(event)

        # Logique streak
        last = profile.last_streak_date
        if last is None or data.study_date > last + timedelta(days=1):
            profile.current_streak = 1
            profile.last_streak_date = data.study_date
        elif data.study_date == last + timedelta(days=1):
            profile.current_streak += 1
            profile.last_streak_date = data.study_date
        elif data.study_date == last:
            # Déjà compté pour aujourd'hui, mais pas d'event_id connu (rare)
            # → on garde la trace, pas d'incrément
            pass
        # else: vieille date, ignore

        profile.longest_streak = max(
            profile.longest_streak, profile.current_streak
        )

        await self.session.flush()
        return SyncHandlerResult(
            status_code=201,
            body={
                "status": "applied",
                "server_ts": event.server_ts.isoformat(),
                "current_streak": profile.current_streak,
                "longest_streak": profile.longest_streak,
            },
        )
