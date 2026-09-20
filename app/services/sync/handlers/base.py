"""Interface commune aux handlers d'entités sync."""

from __future__ import annotations

import abc
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ConflictStrategy, SyncOperation


class SyncHandlerResult:
    """Résultat d'un handler."""

    def __init__(
        self,
        *,
        status_code: int,
        body: dict[str, Any],
    ) -> None:
        self.status_code = status_code
        self.body = body


class SyncHandler(abc.ABC):
    """Contrat pour un handler d'entité."""

    #: Type d'entité géré
    entity_type: str

    #: Stratégie de conflit par défaut
    conflict_strategy: ConflictStrategy

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abc.abstractmethod
    async def apply(
        self,
        *,
        user_id: UUID,
        operation: SyncOperation,
        payload: dict[str, Any],
        client_ts: datetime,
    ) -> SyncHandlerResult:
        """Applique l'opération et retourne (status_code, body)."""
