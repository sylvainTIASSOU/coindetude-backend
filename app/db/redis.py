"""Client Redis async partagé.

Fournit :
- ``redis_client`` : instance unique (pool) pour toute l'application.
- ``get_redis()`` : dépendance FastAPI pour injection.
- ``close_redis()`` : fermeture propre au shutdown.

Utilisation typique :
    from app.db.redis import get_redis
    redis = await get_redis()
    await redis.set("key", "value", ex=60)
"""

from __future__ import annotations

import logging

import redis.asyncio as aioredis
from redis.asyncio import Redis

from app.core.config import settings

logger = logging.getLogger(__name__)

# Pool partagé (créé paresseusement au premier appel)
_redis_client: Redis | None = None


async def get_redis() -> Redis:
    """Retourne le client Redis partagé (création paresseuse).

    Le client utilise un pool de connexions interne ; il est thread-safe
    et doit être réutilisé sur toute la durée de vie de l'application.
    """
    global _redis_client
    if _redis_client is None:
        logger.info(
            "Initialisation du client Redis (%s:%s/%s)",
            settings.REDIS_HOST,
            settings.REDIS_PORT,
            settings.REDIS_DB,
        )
        _redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,  # str au lieu de bytes
            health_check_interval=30,
            socket_keepalive=True,
        )
    return _redis_client


async def close_redis() -> None:
    """Ferme proprement le client Redis (à appeler au shutdown)."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None
        logger.info("Client Redis fermé.")


async def ping_redis() -> bool:
    """Test de connexion (utile pour /health/ready)."""
    try:
        redis = await get_redis()
        return await redis.ping() # type: ignore
    except Exception as exc:  # noqa: BLE001
        logger.warning("Redis ping échoué : %s", exc)
        return False
