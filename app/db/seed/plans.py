"""Seed du catalogue des forfaits Mobile Money.

Idempotent : relançable sans dupliquer les plans.
"""

from __future__ import annotations

import asyncio
import logging
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models import Plan, PlanType

logger = logging.getLogger(__name__)


PLANS: list[dict] = [
    {
        "code": PlanType.FREEMIUM,
        "name": "Découverte",
        "description": "Pour tester CoinDetude sans engagement.",
        "price_fcfa": Decimal("0.00"),
        "duration_days": 0,
        "advantages": [
            "3 scans guidés par jour",
            "Accès à la bibliothèque de base",
            "Planning d'étude limité",
        ],
        "order_index": 1,
    },
    {
        "code": PlanType.PASS_JOUR,
        "name": "Pass Jour",
        "description": "Idéal pour réviser intensivement une journée.",
        "price_fcfa": Decimal("200.00"),
        "duration_days": 1,
        "advantages": [
            "Scans illimités pendant 24h",
            "Tuteur IA complet",
            "Génération de fiches illimitée",
            "Quiz personnalisés",
        ],
        "order_index": 2,
    },
    {
        "code": PlanType.PASS_SEMAINE,
        "name": "Pass Semaine",
        "description": "Une semaine complète pour préparer un devoir.",
        "price_fcfa": Decimal("1000.00"),
        "duration_days": 7,
        "advantages": [
            "Tous les avantages du Pass Jour",
            "7 jours d'accès continu",
            "Économie de 40% vs Pass Jour",
            "Rappels personnalisés",
        ],
        "order_index": 3,
    },
    {
        "code": PlanType.PASS_MOIS,
        "name": "Pass Mois",
        "description": "Le meilleur rapport qualité/prix pour l'année scolaire.",
        "price_fcfa": Decimal("3000.00"),
        "duration_days": 30,
        "advantages": [
            "Tous les avantages du Pass Semaine",
            "30 jours d'accès continu",
            "Économie de 50% vs Pass Jour",
            "Accès prioritaire aux nouveautés",
        ],
        "order_index": 4,
    },
]


async def seed_plans(session: AsyncSession) -> None:
    """Insère les forfaits (idempotent par ``code``)."""
    logger.info("Début du seed des forfaits...")
    for data in PLANS:
        existing = await session.scalar(select(Plan).where(Plan.code == data["code"]))
        if existing:
            continue
        session.add(Plan(**data))
    await session.commit()
    logger.info("Seed des forfaits terminé.")


async def _main() -> None:
    async with AsyncSessionLocal() as session:
        await seed_plans(session)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(_main())
