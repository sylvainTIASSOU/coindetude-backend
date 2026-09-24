"""Schémas Pydantic du profil élève (onboarding + lecture)."""

from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import Cycle
from app.schemas.referential import LevelRead, SeriesRead

# =============================================================================
# Écriture
# =============================================================================

class StudentProfileUpsertRequest(BaseModel):
    """Payload de ``PUT /students/me/profile``.

    Le client envoie le **nom** du niveau et le **code** de la série (pas les
    UUIDs) — plus naturel pour l'onboarding. Le serveur résout les entités.

    **Règles** :
    - ``cycle == college`` → ``series_code`` doit être ``None`` (ou omis).
    - ``cycle != college`` → ``series_code`` optionnel (élève peut compléter
      plus tard), mais si fourni, doit exister ET être autorisé pour ce niveau.
    """

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "summary": "Collégien (3ème)",
                    "value": {
                        "cycle": "college",
                        "level_name": "3ème",
                    },
                },
                {
                    "summary": "Lycéen moderne (Terminale D)",
                    "value": {
                        "cycle": "lycee_moderne",
                        "level_name": "Terminale",
                        "series_code": "D",
                    },
                },
                {
                    "summary": "Lycéen technique (1ère F2)",
                    "value": {
                        "cycle": "lycee_technique",
                        "level_name": "1ère",
                        "series_code": "F2",
                    },
                },
            ]
        },
    )

    cycle: Cycle
    level_name: str = Field(..., min_length=1, max_length=50)
    series_code: str | None = Field(None, min_length=1, max_length=10)

    @model_validator(mode="after")
    def _check_college_has_no_series(self) -> "StudentProfileUpsertRequest":
        if self.cycle is Cycle.COLLEGE and self.series_code:
            raise ValueError(
                "Un collégien ne peut pas avoir de série. "
                "Laisse `series_code` vide pour le cycle `college`."
            )
        return self


# =============================================================================
# Lecture
# =============================================================================

class StudentProfileRead(BaseModel):
    """Vue complète du profil élève (avec entités imbriquées)."""

    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    level: LevelRead | None = None
    series: SeriesRead | None = None
    xp_points: int
    current_streak: int
    longest_streak: int
    last_streak_date: date | None = None
    pairing_code: str = Field(
        ..., description="Code à 6 caractères pour lier un parent (privé)"
    )


class StudentProfilePublic(BaseModel):
    """Vue du profil élève pour un tiers (parent).

    ⚠️ Le ``pairing_code`` est **omis** (donnée sensible).
    """

    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    first_name: str
    last_name: str
    level: LevelRead | None = None
    series: SeriesRead | None = None
    xp_points: int
    current_streak: int
    longest_streak: int


# =============================================================================
# Options d'onboarding
# =============================================================================

class LevelWithSeries(BaseModel):
    """Niveau + séries autorisées pour ce niveau."""

    level: LevelRead
    series: list[SeriesRead] = Field(
        default_factory=list,
        description="Vide pour les niveaux du collège",
    )


class CycleOptions(BaseModel):
    """Toutes les options d'un cycle."""

    cycle: Cycle
    levels: list[LevelWithSeries]


class ProfileOptionsResponse(BaseModel):
    """Réponse de ``GET /students/me/profile/options``.

    Fournit au client toutes les données nécessaires pour l'onboarding en
    un seul appel (frugalité réseau).
    """

    cycles: list[CycleOptions]
    cache_ttl: int = Field(..., description="TTL recommandé côté client (s)")
