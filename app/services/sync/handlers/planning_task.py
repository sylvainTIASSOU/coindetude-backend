"""Handler LWW field-level pour ``planning_task``.

**Stratégie** : LWW au niveau de l'entité avec application sélective des champs.

Le client envoie uniquement les champs modifiés (``payload``). Le serveur
compare ``client_ts`` à ``StudyPlanning.updated_at`` :

- ``client_ts > updated_at`` → le client gagne, les champs sont appliqués.
- ``client_ts <= updated_at`` → le serveur gagne, on retourne 409 avec
  ``server_state`` complet.

**Create** : insertion du nouvel enregistrement. Si l'id existe déjà → on
bascule en update LWW.

**Delete** : suppression si ``client_ts > updated_at``, sinon 409.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import select

from app.models import PlanningEventType, StudyPlanning
from app.models.enums import ConflictStrategy, SyncOperation
from app.services.sync.errors import ConflictDetected, SyncError
from app.services.sync.handlers.base import SyncHandler, SyncHandlerResult


class PlanningTaskPayload(BaseModel):
    """Payload attendu pour ``planning_task``."""
    id: UUID
    title: str | None = Field(None, min_length=1, max_length=255)
    event_type: PlanningEventType | None = None
    scheduled_date: datetime | None = None
    is_completed: bool | None = None


def _serialize_task(task: StudyPlanning) -> dict[str, Any]:
    return {
        "id": str(task.id),
        "title": task.title,
        "event_type": task.event_type.value,
        "scheduled_date": task.scheduled_date.isoformat(),
        "is_completed": task.is_completed,
        "updated_at": task.updated_at.isoformat(),
    }


class PlanningTaskHandler(SyncHandler):
    entity_type = "planning_task"
    conflict_strategy = ConflictStrategy.LWW

    async def apply(
        self,
        *,
        user_id: UUID,
        operation: SyncOperation,
        payload: dict[str, Any],
        client_ts: datetime,
    ) -> SyncHandlerResult:
        try:
            data = PlanningTaskPayload.model_validate(payload)
        except ValidationError as exc:
            raise SyncError(
                detail=f"Payload invalide : {exc.errors()[0]['msg']}",
                status_code=422,
            ) from exc

        existing = await self.session.scalar(
            select(StudyPlanning).where(
                StudyPlanning.id == data.id,
                StudyPlanning.student_id == user_id,
            )
        )

        # ---------- DELETE ----------
        if operation is SyncOperation.DELETE:
            if existing is None:
                # Déjà supprimé → idempotent, considéré appliqué
                return SyncHandlerResult(
                    status_code=200,
                    body={"status": "applied", "deduplicated": True},
                )
            if client_ts <= existing.updated_at:
                raise ConflictDetected(
                    server_state=_serialize_task(existing),
                    strategy=self.conflict_strategy,
                )
            await self.session.delete(existing)
            await self.session.flush()
            return SyncHandlerResult(
                status_code=200,
                body={
                    "status": "applied",
                    "server_ts": datetime.now().astimezone().isoformat(),
                },
            )

        # ---------- CREATE ----------
        if operation is SyncOperation.CREATE:
            if existing is not None:
                # Course : l'entité existe déjà. On bascule en update LWW.
                return await self._apply_update(
                    existing=existing, data=data, client_ts=client_ts
                )

            task = StudyPlanning(
                id=data.id,
                student_id=user_id,
                title=data.title or "Sans titre",
                event_type=data.event_type or PlanningEventType.REVISION,
                scheduled_date=data.scheduled_date or client_ts,
                is_completed=data.is_completed or False,
            )
            self.session.add(task)
            await self.session.flush()
            return SyncHandlerResult(
                status_code=201,
                body={
                    "status": "applied",
                    "server_ts": task.updated_at.isoformat(),
                },
            )

        # ---------- UPDATE ----------
        if operation is SyncOperation.UPDATE:
            if existing is None:
                raise SyncError(
                    detail="Entité introuvable pour update.",
                    status_code=404,
                )
            return await self._apply_update(
                existing=existing, data=data, client_ts=client_ts
            )

        raise SyncError(detail=f"Opération inconnue : {operation}", status_code=400)

    async def _apply_update(
        self,
        *,
        existing: StudyPlanning,
        data: PlanningTaskPayload,
        client_ts: datetime,
    ) -> SyncHandlerResult:
        """LWW : applique les champs si client_ts > existing.updated_at."""
        if client_ts <= existing.updated_at:
            raise ConflictDetected(
                server_state=_serialize_task(existing),
                strategy=self.conflict_strategy,
            )

        if data.title is not None:
            existing.title = data.title
        if data.event_type is not None:
            existing.event_type = data.event_type
        if data.scheduled_date is not None:
            existing.scheduled_date = data.scheduled_date
        if data.is_completed is not None:
            existing.is_completed = data.is_completed
        # Force updated_at à client_ts (LWW)
        from app.core.security import utcnow
        existing.updated_at = max(client_ts, utcnow())

        await self.session.flush()
        return SyncHandlerResult(
            status_code=200,
            body={
                "status": "applied",
                "server_ts": existing.updated_at.isoformat(),
            },
        )
