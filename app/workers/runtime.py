"""Contexte partagé par les jobs ARQ.

ARQ injecte un dict ``ctx`` dans chaque job. On y met :

- ``redis`` : client Redis partagé (broker + queues applicatives)
- ``session_maker`` : ``async_sessionmaker`` partagé
- ``s3`` : client S3
- ``posthog_client`` : client httpx.AsyncClient réutilisé

Créés au ``startup`` et fermés au ``shutdown`` du worker.
"""

from __future__ import annotations

from typing import Any

import httpx
import redis.asyncio as aioredis
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.services.storage.s3_client import S3Client, get_s3_client

from app.core.logging import log as logger


def _broker_redis_url() -> str: # type: ignore
    """URL Redis pour le broker ARQ (DB dédiée)."""
    base = settings.REDIS_URL.rsplit("/", 1)[0]
    return f"{base}/{settings.WORKER_REDIS_DB}"


async def startup(ctx: dict[str, Any]) -> None:
    """Initialise les ressources partagées du worker."""
    logger.info("🚀 Worker ARQ démarrage…")

    # Redis applicatif (queues, caches)
    ctx["redis"] = aioredis.from_url( # type: ignore
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        health_check_interval=30,
    )

    # Session DB
    ctx["session_maker"]: async_sessionmaker = AsyncSessionLocal # type: ignore

    # Client S3
    ctx["s3"]: S3Client = get_s3_client() # type: ignore

    # Client HTTPX partagé (PostHog)
    ctx["http"] = httpx.AsyncClient(timeout=10.0)

    logger.info("✅ Worker ARQ prêt.")


async def shutdown(ctx: dict[str, Any]) -> None:
    """Ferme proprement les ressources."""
    logger.info("🛑 Worker ARQ arrêt…")
    redis: Redis | None = ctx.get("redis")
    if redis:
        await redis.aclose()
    http: httpx.AsyncClient | None = ctx.get("http")
    if http:
        await http.aclose()
    logger.info("Worker ARQ arrêté.")


def broker_settings() -> dict[str, Any]:
    """Settings passés à ARQ pour la connexion Redis."""
    return {
        "host": settings.REDIS_HOST,
        "port": settings.REDIS_PORT,
        "database": settings.WORKER_REDIS_DB,
        "password": settings.REDIS_PASSWORD,
    }
