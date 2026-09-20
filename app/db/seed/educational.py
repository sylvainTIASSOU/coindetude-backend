"""Seed du référentiel pédagogique togolais.

Ce module insère :
- Les niveaux (collège 6/5/4/3, lycée moderne 2nde/1ère/Term, lycée technique idem)
- Les séries (A, C, S en 2nde moderne ; A4, C, D en 1ère/Term moderne ;
  T en 2nde technique ; F1/F2/F3/F4 en 1ère/Term technique)
- Les associations niveau ↔ série (``level_series``)

**Idempotence** : chaque insertion vérifie l'existence par clé naturelle
avant de créer. Le seed peut être relancé sans dupliquer les données.

Usage :
    python -m app.db.seed.educational
"""

from __future__ import annotations

import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal  # à adapter selon ton projet
from app.models import Cycle, Level, LevelSeries, Series

logger = logging.getLogger(__name__)


# --- Niveaux ---
LEVELS: list[tuple[str, Cycle, int]] = [
    # Collège
    ("6ème", Cycle.COLLEGE, 1),
    ("5ème", Cycle.COLLEGE, 2),
    ("4ème", Cycle.COLLEGE, 3),
    ("3ème", Cycle.COLLEGE, 4),
    # Lycée moderne
    ("2nde", Cycle.LYCEE_MODERNE, 5),
    ("1ère", Cycle.LYCEE_MODERNE, 6),
    ("Terminale", Cycle.LYCEE_MODERNE, 7),
    # Lycée technique
    ("2nde", Cycle.LYCEE_TECHNIQUE, 5),
    ("1ère", Cycle.LYCEE_TECHNIQUE, 6),
    ("Terminale", Cycle.LYCEE_TECHNIQUE, 7),
]


# --- Séries ---
# (code, name, cycle)
SERIES: list[tuple[str, str, Cycle]] = [
    # Lycée moderne
    ("A", "Série A - Littéraire (2nde)", Cycle.LYCEE_MODERNE),
    ("C", "Série C - Mathématiques et Sciences Physiques", Cycle.LYCEE_MODERNE),
    ("S", "Série S - Sciences (2nde)", Cycle.LYCEE_MODERNE),
    ("A4", "Série A4 - Littéraire et Langues", Cycle.LYCEE_MODERNE),
    ("D", "Série D - Mathématiques et Sciences de la Nature", Cycle.LYCEE_MODERNE),
    # Lycée technique
    ("T", "Série T - Technologie (2nde)", Cycle.LYCEE_TECHNIQUE),
    ("F1", "Série F1 - Construction Mécanique", Cycle.LYCEE_TECHNIQUE),
    ("F2", "Série F2 - Électronique", Cycle.LYCEE_TECHNIQUE),
    ("F3", "Série F3 - Électrotechnique", Cycle.LYCEE_TECHNIQUE),
    ("F4", "Série F4 - Génie Civil", Cycle.LYCEE_TECHNIQUE),
]


# --- Associations (level_name, level_cycle, series_code, series_cycle) ---
LEVEL_SERIES: list[tuple[str, Cycle, str, Cycle]] = [
    # Lycée moderne
    ("2nde", Cycle.LYCEE_MODERNE, "A", Cycle.LYCEE_MODERNE),
    ("2nde", Cycle.LYCEE_MODERNE, "C", Cycle.LYCEE_MODERNE),
    ("2nde", Cycle.LYCEE_MODERNE, "S", Cycle.LYCEE_MODERNE),
    ("1ère", Cycle.LYCEE_MODERNE, "A4", Cycle.LYCEE_MODERNE),
    ("1ère", Cycle.LYCEE_MODERNE, "C", Cycle.LYCEE_MODERNE),
    ("1ère", Cycle.LYCEE_MODERNE, "D", Cycle.LYCEE_MODERNE),
    ("Terminale", Cycle.LYCEE_MODERNE, "A4", Cycle.LYCEE_MODERNE),
    ("Terminale", Cycle.LYCEE_MODERNE, "C", Cycle.LYCEE_MODERNE),
    ("Terminale", Cycle.LYCEE_MODERNE, "D", Cycle.LYCEE_MODERNE),
    # Lycée technique
    ("2nde", Cycle.LYCEE_TECHNIQUE, "T", Cycle.LYCEE_TECHNIQUE),
    ("1ère", Cycle.LYCEE_TECHNIQUE, "F1", Cycle.LYCEE_TECHNIQUE),
    ("1ère", Cycle.LYCEE_TECHNIQUE, "F2", Cycle.LYCEE_TECHNIQUE),
    ("1ère", Cycle.LYCEE_TECHNIQUE, "F3", Cycle.LYCEE_TECHNIQUE),
    ("1ère", Cycle.LYCEE_TECHNIQUE, "F4", Cycle.LYCEE_TECHNIQUE),
    ("Terminale", Cycle.LYCEE_TECHNIQUE, "F1", Cycle.LYCEE_TECHNIQUE),
    ("Terminale", Cycle.LYCEE_TECHNIQUE, "F2", Cycle.LYCEE_TECHNIQUE),
    ("Terminale", Cycle.LYCEE_TECHNIQUE, "F3", Cycle.LYCEE_TECHNIQUE),
    ("Terminale", Cycle.LYCEE_TECHNIQUE, "F4", Cycle.LYCEE_TECHNIQUE),
]


async def seed_educational(session: AsyncSession) -> None:
    """Insère niveaux, séries et associations (idempotent)."""
    logger.info("Début du seed pédagogique...")

    # --- Niveaux ---
    level_map: dict[tuple[str, Cycle], Level] = {}
    for name, cycle, order in LEVELS:
        existing = await session.scalar(
            select(Level).where(Level.name == name, Level.cycle == cycle)
        )
        if existing:
            level_map[(name, cycle)] = existing
            continue
        level = Level(name=name, cycle=cycle, order_index=order)
        session.add(level)
        level_map[(name, cycle)] = level
    await session.flush()
    logger.info("Niveaux : %d", len(level_map))

    # --- Séries ---
    series_map: dict[tuple[str, Cycle], Series] = {}
    for code, name, cycle in SERIES:
        existing = await session.scalar(
            select(Series).where(Series.code == code, Series.cycle == cycle)
        )
        if existing:
            series_map[(code, cycle)] = existing
            continue
        s = Series(code=code, name=name, cycle=cycle)
        session.add(s)
        series_map[(code, cycle)] = s
    await session.flush()
    logger.info("Séries : %d", len(series_map))

    # --- Associations ---
    inserted = 0
    for level_name, level_cycle, series_code, series_cycle in LEVEL_SERIES:
        level = level_map[(level_name, level_cycle)]
        s = series_map[(series_code, series_cycle)]
        existing = await session.scalar(
            select(LevelSeries).where(
                LevelSeries.level_id == level.id,
                LevelSeries.series_id == s.id,
            )
        )
        if existing:
            continue
        session.add(LevelSeries(level_id=level.id, series_id=s.id))
        inserted += 1
    await session.flush()
    logger.info("Associations ajoutées : %d", inserted)

    await session.commit()
    logger.info("Seed pédagogique terminé.")


async def _main() -> None:
    async with AsyncSessionLocal() as session:
        await seed_educational(session)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(_main())
