"""Service d'idempotence stricte pour les endpoints critiques.

**Principe** :

1. Le client envoie un header ``Idempotency-Key`` (UUID v4).
2. Le serveur calcule le SHA-256 du body.
3. Si la clé existe déjà avec le même hash → on retourne la réponse stockée.
4. Si la clé existe avec un hash différent → 409 (abus).
5. Sinon → on exécute, on stocke la réponse, on retourne.

**Concurrence** :

Un verrou Redis (``SET NX EX``) empêche deux requêtes simultanées avec la même
clé de s'exécuter en parallèle. La 2e reçoit un 409 avec ``Retry-After``.

**TTL** : 7 jours (aligné sur la fenêtre ``client_ts``).
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Callable, Awaitable
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import utcnow
from app.models import IdempotencyKey
from app.services.sync.errors import (
    IdempotencyInFlight,
    IdempotencyKeyConflict,
)

logger = logging.getLogger(__name__)

IDEMPOTENCY_TTL_DAYS = 7
LOCK_TTL_SECONDS = 30


@dataclass(frozen=True, slots=True)
class StoredResponse:
    """Réponse stockée, prête à être rejouée."""
    status_code: int
    body: dict[str, Any]


def compute_request_hash(body: bytes | dict[str, Any] | str) -> str:
    """SHA-256 hex du body, stable quelle que soit la sérialisation."""
    if isinstance(body, bytes):
        raw = body
    elif isinstance(body, str):
        raw = body.encode("utf-8")
    else:
        # Sort_keys + séparateurs compacts pour garantir la stabilité
        raw = json.dumps(
            body, sort_keys=True, separators=(",", ":"), default=str
        ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


class IdempotencyService:
    def __init__(self, session: AsyncSession, redis: Redis) -> None:
        self.session = session
        self.redis = redis

    def _lock_key(self, user_id: UUID, scope: str, key: str) -> str:
        return f"idem:lock:{user_id}:{scope}:{key}"

    async def _fetch(
        self, *, user_id: UUID, scope: str, key: str
    ) -> IdempotencyKey | None:
        stmt = select(IdempotencyKey).where(
            IdempotencyKey.user_id == user_id,
            IdempotencyKey.scope == scope,
            IdempotencyKey.key == key,
        )
        row = await self.session.scalar(stmt)
        # TTL applicatif (nettoyage paresseux)
        if row is not None and row.expires_at <= utcnow():
            await self.session.delete(row)
            await self.session.flush()
            return None
        return row

    async def execute(
        self,
        *,
        user_id: UUID,
        scope: str,
        key: str,
        request_body: dict[str, Any],
        handler: Callable[[], Awaitable[tuple[int, dict[str, Any]]]],
    ) -> tuple[StoredResponse, bool]:
        """Exécute ``handler`` avec idempotence stricte.

        Returns:
            (StoredResponse, is_replay) — ``is_replay=True`` si la réponse
            provient du cache d'idempotence.
        """
        request_hash = compute_request_hash(request_body)

        # 1. Vérifier l'existant (chemin rapide)
        existing = await self._fetch(user_id=user_id, scope=scope, key=key)
        if existing is not None:
            if existing.request_hash != request_hash:
                raise IdempotencyKeyConflict()
            logger.info(
                "Idempotency replay (user=%s scope=%s key=%s...)",
                user_id, scope, key[:8],
            )
            return (
                StoredResponse(existing.response_status, existing.response_body),
                True,
            )

        # 2. Acquérir le verrou
        lock_key = self._lock_key(user_id, scope, key)
        acquired = await self.redis.set(lock_key, "1", nx=True, ex=LOCK_TTL_SECONDS)
        if not acquired:
            # Attendre un court instant puis retenter une lecture
            await asyncio.sleep(1.0)
            existing = await self._fetch(user_id=user_id, scope=scope, key=key)
            if existing is not None:
                if existing.request_hash != request_hash:
                    raise IdempotencyKeyConflict()
                return (
                    StoredResponse(existing.response_status, existing.response_body),
                    True,
                )
            raise IdempotencyInFlight()

        try:
            # 3. Double-checked locking
            existing = await self._fetch(user_id=user_id, scope=scope, key=key)
            if existing is not None:
                if existing.request_hash != request_hash:
                    raise IdempotencyKeyConflict()
                return (
                    StoredResponse(existing.response_status, existing.response_body),
                    True,
                )

            # 4. Exécuter
            status_code, body = await handler()

            # 5. Stocker (uniquement pour les non-5xx)
            if status_code < 500:
                stored = IdempotencyKey(
                    user_id=user_id,
                    scope=scope,
                    key=key,
                    request_hash=request_hash,
                    response_status=status_code,
                    response_body=body,
                    expires_at=utcnow() + timedelta(days=IDEMPOTENCY_TTL_DAYS),
                )
                self.session.add(stored)
                try:
                    await self.session.flush()
                except IntegrityError:
                    # Course concurrente extrêmement rare : on relit
                    await self.session.rollback()
                    existing = await self._fetch(
                        user_id=user_id, scope=scope, key=key
                    )
                    if existing is None:
                        raise
                    return (
                        StoredResponse(
                            existing.response_status, existing.response_body
                        ),
                        True,
                    )

            return StoredResponse(status_code, body), False
        finally:
            await self.redis.delete(lock_key)
