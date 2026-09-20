"""Runner de seed automatique.

Lance les seeds pédagogiques et plans **en arrière-plan** au démarrage de
l'application, sans bloquer le boot. Utilise une clé Redis comme verrou
distribué pour :

1. Éviter de re-seeder à chaque redémarrage (idempotence globale).
2. Éviter la concurrence si plusieurs workers Uvicorn démarrent en parallèle
   (Gunicorn multi-worker ou déploiement multi-instance).

**Fonctionnement** :

- Clé Redis ``coindetude:seed:completed`` : marqueur "seed déjà fait".
- Clé Redis ``coindetude:seed:lock`` : verrou à TTL court pour éviter que
  2 workers lancent le seed en même temps.
- Si le marqueur existe → on ne fait rien.
- Sinon, on tente d'acquérir le verrou. Si succès → on exécute les seeds
  et on pose le marqueur. Si échec → un autre worker s'en occupe.
"""

from __future__ import annotations

import asyncio
import logging

from app.core.config import settings
from app.db.redis import get_redis
from app.db.seed.educational import seed_educational
from app.db.seed.plans import seed_plans
from app.db.session import AsyncSessionLocal

logger = logging.getLogger(__name__)

SEED_COMPLETED_KEY = "coindetude:seed:completed"
SEED_LOCK_KEY = "coindetude:seed:lock"


async def _run_seeds() -> None:
    """Exécute tous les seeds dans une transaction dédiée."""
    async with AsyncSessionLocal() as session:
        await seed_educational(session)
        await seed_plans(session)


async def run_auto_seed() -> None:
    """Point d'entrée du seed automatique.

    Ne lève jamais d'exception : toute erreur est loguée mais ne doit pas
    empêcher l'application de démarrer.
    """
    if not settings.AUTO_SEED_ENABLED:
        logger.info("Seed automatique désactivé (AUTO_SEED_ENABLED=False).")
        return

    try:
        redis = await get_redis()

        # 1. Vérifier si le seed a déjà été fait
        already_done = await redis.exists(SEED_COMPLETED_KEY)
        if already_done:
            logger.info("Seed déjà effectué (marqueur Redis présent). Skip.")
            return

        # 2. Tenter d'acquérir le verrou (SET NX EX)
        lock_acquired = await redis.set(
            SEED_LOCK_KEY,
            "1",
            nx=True,
            ex=settings.AUTO_SEED_LOCK_TTL_SECONDS,
        )
        if not lock_acquired:
            logger.info(
                "Seed déjà en cours par un autre worker (verrou Redis présent). Skip."
            )
            return

        # 3. Exécuter les seeds
        logger.info("Démarrage du seed automatique...")
        await _run_seeds()

        # 4. Poser le marqueur "seed fait" (permanent, pas de TTL)
        await redis.set(SEED_COMPLETED_KEY, "1")
        logger.info("Seed automatique terminé avec succès.")

    except Exception as exc:  # noqa: BLE001
        logger.exception("Échec du seed automatique : %s", exc)
        # On ne propage pas : l'app doit démarrer même si le seed échoue.
    finally:
        # Libérer le verrou s'il est encore posé (au cas où le seed a planté)
        try:
            redis = await get_redis()
            # Ne supprime le verrou que si le marqueur "completed" n'est PAS posé
            # (sinon on risquerait de supprimer un verrou légitime d'un autre worker)
            completed = await redis.exists(SEED_COMPLETED_KEY)
            if not completed:
                await redis.delete(SEED_LOCK_KEY)
        except Exception:  # noqa: BLE001
            pass


def schedule_auto_seed() -> asyncio.Task[None]:
    """Planifie le seed en tâche de fond (non bloquant).

    Retourne la ``Task`` pour permettre au lifespan de l'annuler proprement
    au shutdown si nécessaire.
    """
    return asyncio.create_task(run_auto_seed(), name="auto-seed")
