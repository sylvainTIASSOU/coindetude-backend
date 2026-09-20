"""Configuration ARQ (WorkerSettings).

Expose les fonctions + les cron jobs à exécuter.

**Lancement** :

    arq app.workers.settings.WorkerSettings

**Ou via Docker Compose** : service ``worker`` (voir docker-compose.yml).
"""

from __future__ import annotations

from arq import cron
from arq.connections import RedisSettings

from app.core.config import settings
from app.workers.purges import (
    deactivate_expired_subscriptions,
    purge_expired_idempotency,
    purge_expired_otp,
    purge_pending_uploads,
)
from app.workers.runtime import shutdown, startup
from app.workers.telemetry_consumer import telemetry_consumer


def _redis_settings() -> RedisSettings:
    return RedisSettings(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        database=settings.WORKER_REDIS_DB,
        password=settings.REDIS_PASSWORD,
    )


class WorkerSettings:
    """Settings ARQ. Référencé par ``arq app.workers.settings.WorkerSettings``."""

    redis_settings = _redis_settings()

    # Jobs appelables à la demande (par `enqueue_job`)
    functions = [
        telemetry_consumer,
        purge_expired_otp,
        purge_expired_idempotency,
        purge_pending_uploads,
        deactivate_expired_subscriptions,
    ]

    # Jobs planifiés (cron)
    cron_jobs = [
        # Telemetry : toutes les minutes
        cron(telemetry_consumer, minute=set(range(60)), run_at_startup=True),
        # Purges : toutes les heures à minute 5
        cron(purge_expired_otp, minute={5}),
        cron(purge_expired_idempotency, minute={5}),
        cron(purge_pending_uploads, minute={5}),
        # Subscriptions : toutes les 15 minutes
        cron(
            deactivate_expired_subscriptions,
            minute={0, 15, 30, 45},
        ),
    ]

    on_startup = startup
    on_shutdown = shutdown
    max_jobs = settings.WORKER_MAX_JOBS
    job_timeout = settings.WORKER_JOB_TIMEOUT_SECONDS
    keep_result = settings.WORKER_KEEP_RESULT_SECONDS
    health_check_interval = 60  # secondes
