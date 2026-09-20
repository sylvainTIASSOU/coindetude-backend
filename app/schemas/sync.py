"""Schémas Pydantic pour ``/sync/apply-event``."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import (
    ConflictStrategy,
    SyncEntityType,
    SyncOperation,
)


class SyncEventRequest(BaseModel):
    """Requête POST /sync/apply-event.

    ⚠️ ``payload`` est un objet JSON direct (pas une string échappée).
    Cela réduit la taille du body (~30%) et évite les erreurs de parsing.
    """

    model_config = ConfigDict(extra="forbid")

    entity_type: SyncEntityType
    operation: SyncOperation
    payload: dict[str, Any] = Field(
        ...,
        description="Contenu de l'entité (objet JSON direct)",
    )
    client_ts: datetime = Field(
        ...,
        description="Horodatage client ISO 8601 UTC (tolérance ±7 jours)",
    )


class SyncEventAppliedResponse(BaseModel):
    """Réponse 200/201 sur succès."""

    status: Literal["applied"] = "applied"
    server_ts: str | None = None
    deduplicated: bool | None = None
    # Champs spécifiques à certains handlers
    new_xp_total: int | None = None
    current_streak: int | None = None
    longest_streak: int | None = None


class SyncEventConflictResponse(BaseModel):
    """Réponse 409 sur conflit LWW/MANUAL."""

    status: Literal["conflict"] = "conflict"
    server_state: dict[str, Any]
    conflict_strategy: ConflictStrategy
