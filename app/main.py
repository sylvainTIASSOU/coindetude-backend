"""Point d'entrée FastAPI de CoinDetude.

Gère le cycle de vie de l'application :
- Startup : initialisation Redis, scheduling du seed automatique.
- Shutdown : fermeture propre des connexions (Redis, DB).

Le seed est lancé **en arrière-plan** pour ne pas bloquer le démarrage
(cf. ``app/db/seed/runner.py``).
"""

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging, log
from app.db.redis import close_redis, ping_redis
from app.db.seed.runner import schedule_auto_seed


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    configure_logging()
    """Gestion du cycle de vie de l'application."""
    # --- Startup ---
    log.info(
        "Démarrage de %s v%s (%s)",
        settings.PROJECT_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )

    # 1. Vérifier la connexion Redis (mais ne pas bloquer si KO en dev)
    redis_ok = await ping_redis()
    if not redis_ok:
        log.warning(
            "Redis injoignable au démarrage. Le rate limiting et le cache "
            "seront indisponibles tant que Redis ne répond pas."
        )
        # Créer le bucket S3 en dev (idempotent)
    if settings.S3_AUTO_CREATE_BUCKET_IN_DEV and settings.ENVIRONMENT == "dev":
        from app.services.storage.s3_client import get_s3_client
        try:
            await get_s3_client().ensure_bucket_exists()
        except Exception as exc:  # noqa: BLE001
            log.warning("Bootstrap bucket S3 échoué : %s", exc)
    # 2. Planifier le seed automatique en arrière-plan
    seed_task: asyncio.Task[None] | None = None
    if settings.AUTO_SEED_ENABLED and redis_ok:
        seed_task = schedule_auto_seed()
        log.info("Seed automatique planifié en arrière-plan.")
    elif not redis_ok:
        log.warning("Seed automatique annulé : Redis requis pour le verrou distribué.")

    yield

    # --- Shutdown ---
    log.info("Arrêt de l'application...")

    # Annuler le seed s'il est encore en cours
    if seed_task is not None and not seed_task.done():
        seed_task.cancel()
        try:
            await seed_task
        except asyncio.CancelledError:
            log.info("Seed automatique annulé au shutdown.")

    # Fermer Redis proprement
    await close_redis()
    log.info("Shutdown terminé.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs" if settings.ENVIRONMENT != "prod" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "prod" else None,
    lifespan=lifespan,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
