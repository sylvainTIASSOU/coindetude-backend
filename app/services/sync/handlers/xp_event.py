"""Handler CRDT additif pour ``xp_event``.

**Stratégie** : append-only, déduplication par ``event_id``.

- Si ``event_id`` inconnu → insertion + incrément de ``student.xp_points``.
- Si ``event_id`` connu → ``deduplicated=True`` sans modification.

Aucun 409 possible : c'est un CRDT (commutatif, idempotent, associatif).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import select

from app.models import StudentProfile, UserEvent, UserEventKind
from app.models.enums import ConflictStrategy, SyncOperation
from app.services.sync.errors import SyncError
from app.services.sync.handlers.base import SyncHandler, SyncHandlerResult


class XPEventPayload(BaseModel):
    """Payload attendu pour ``xp_event``."""
    event_id: UUID
    amount: int = Field(..., gt=0, le=1000, description="XP gagnés (1-1000)")
    reason: str = Field(..., min_length=1, max_length=100)


class XPEventHandler(SyncHandler):
    entity_type = "xp_event"
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
                detail="xp_event supporte uniquement l'opération 'create'.",
                status_code=422,
            )
        try:
            data = XPEventPayload.model_validate(payload)
        except ValidationError as exc:
            raise SyncError(
                detail=f"Payload invalide : {exc.errors()[0]['msg']}",
                status_code=422,
            ) from exc

        # Dédup
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

        # Insertion
        event = UserEvent(
            event_id=data.event_id,
            student_id=user_id,
            kind=UserEventKind.XP_ADDED,
            amount=data.amount,
            reason=data.reason,
            event_ts=client_ts,
            payload={"reason": data.reason},
        )
        self.session.add(event)

        # Incrément XP
        profile = await self.session.get(StudentProfile, user_id)
        if profile is None:
            raise SyncError(
                detail="Profil élève introuvable.", status_code=404
            )
        profile.xp_points += data.amount

        await self.session.flush()
        return SyncHandlerResult(
            status_code=201,
            body={
                "status": "applied",
                "server_ts": event.server_ts.isoformat(),
                "new_xp_total": profile.xp_points,
            },
        )
