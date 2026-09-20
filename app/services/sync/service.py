"""Orchestrateur du endpoint ``/sync/apply-event``.

**Flow** :

1. Vérifier la fenêtre ``client_ts`` (±7 jours).
2. Router vers le handler de l'entité.
3. Exécuter le handler dans le contexte d'idempotence.
4. Gérer les conflits (``ConflictDetected``) → 409 + ``server_state``.
5. Retourner la réponse (``applied`` ou ``conflict``).
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import utcnow
from app.models.enums import ConflictStrategy, SyncEntityType, SyncOperation
from app.services.sync.errors import (
    ClientTimestampOutOfWindow,
    ConflictDetected,
    SyncError,
)
from app.services.sync.handlers import HANDLERS
from app.services.sync.idempotency import IdempotencyService

logger = logging.getLogger(__name__)

CLIENT_TS_WINDOW = timedelta(days=7)
IDEMPOTENCY_SCOPE = "sync:apply-event"


class SyncService:
    def __init__(self, session: AsyncSession, redis: Redis) -> None:
        self.session = session
        self.redis = redis
        self.idempotency = IdempotencyService(session, redis)

    async def apply_event(
        self,
        *,
        user_id: UUID,
        idempotency_key: str,
        entity_type: SyncEntityType,
        operation: SyncOperation,
        payload: dict[str, Any],
        client_ts: datetime,
    ) -> tuple[int, dict[str, Any], bool]:
        """Applique un événement avec idempotence.

        Returns:
            (status_code, response_body, is_replay)
        """
        # 1. Fenêtre client_ts
        self._check_client_ts(client_ts)

        # 2. Handler
        handler_cls = HANDLERS.get(entity_type)
        if handler_cls is None:
            raise SyncError(
                detail=f"Type d'entité inconnu : {entity_type.value}",
                status_code=422,
            )
        handler = handler_cls(self.session)

        # 3. Exécution idempotente
        async def _run() -> tuple[int, dict[str, Any]]:
            try:
                result = await handler.apply(
                    user_id=user_id,
                    operation=operation,
                    payload=payload,
                    client_ts=client_ts,
                )
                return result.status_code, result.body
            except ConflictDetected as conflict:
                return 409, {
                    "status": "conflict",
                    "server_state": conflict.server_state,
                    "conflict_strategy": conflict.strategy.value,
                }

        request_body = {
            "entity_type": entity_type.value,
            "operation": operation.value,
            "payload": payload,
            "client_ts": client_ts.isoformat(),
        }
        stored, is_replay = await self.idempotency.execute(
            user_id=user_id,
            scope=IDEMPOTENCY_SCOPE,
            key=idempotency_key,
            request_body=request_body,
            handler=_run,
        )
        return stored.status_code, stored.body, is_replay

    def _check_client_ts(self, client_ts: datetime) -> None:
        """Vérifie que ``client_ts`` est dans ±7 jours.

        Les dates futures sont **clampées** à maintenant pour éviter les
        abus de type « je gagne toujours le LWW ».
        """
        now = utcnow()
        delta = now - client_ts
        if abs(delta) > CLIENT_TS_WINDOW:
            raise ClientTimestampOutOfWindow()
