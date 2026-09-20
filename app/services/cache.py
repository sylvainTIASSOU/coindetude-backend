"""Cache Redis versionné pour le référentiel pédagogique.

**Problème** : invalider un cache Redis par pattern (`SCAN` + `DEL`) est lent
et bloque Redis sur de gros volumes.

**Solution** : versioning par entité.
- Une clé ``ref:v:{entity}`` contient un compteur global.
- Chaque entrée de cache a une clé ``ref:{entity}:v{version}:{filters_hash}``.
- Invalider = ``INCR ref:v:{entity}`` (O(1)).
- Les anciennes clés expirent naturellement via TTL (1h).

**Impact** : zéro coût d'invalidation, aucune race condition.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from redis.asyncio import Redis

from app.core.logging import log as logger

CACHE_TTL_SECONDS = 3600
VERSION_KEY_PREFIX = "ref:v:"
CACHE_KEY_PREFIX = "ref:"


class ReferentialCache:
    """Helper de cache versionné pour les entités du référentiel."""

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    @staticmethod
    def _filters_hash(filters: dict[str, Any]) -> str:
        """Hash stable des filtres (pour construire une clé unique)."""
        raw = json.dumps(filters, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    async def _get_version(self, entity: str) -> int:
        """Retourne la version courante d'une entité (0 par défaut)."""
        raw = await self.redis.get(f"{VERSION_KEY_PREFIX}{entity}")
        return int(raw) if raw else 0

    async def _build_key(self, entity: str, filters: dict[str, Any]) -> str:
        version = await self._get_version(entity)
        return f"{CACHE_KEY_PREFIX}{entity}:v{version}:{self._filters_hash(filters)}"

    async def get(self, entity: str, filters: dict[str, Any]) -> dict[str, Any] | None:
        """Récupère une entrée cachée, ou None."""
        key = await self._build_key(entity, filters)
        raw = await self.redis.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("Cache corrompu pour %s, ignore", key)
            return None

    async def set(
        self,
        entity: str,
        filters: dict[str, Any],
        value: dict[str, Any],
        ttl: int = CACHE_TTL_SECONDS,
    ) -> None:
        """Stocke une entrée cachée avec TTL."""
        key = await self._build_key(entity, filters)
        await self.redis.set(key, json.dumps(value, default=str), ex=ttl)

    async def invalidate(self, entity: str) -> None:
        """Invalide tout le cache d'une entité (incrément de version)."""
        await self.redis.incr(f"{VERSION_KEY_PREFIX}{entity}")
        logger.info("Cache invalidé pour entity=%s", entity)


def cache_control_header() -> dict[str, str]:
    """Header Cache-Control standard pour les endpoints publics."""
    return {"Cache-Control": "public, max-age=3600"}
