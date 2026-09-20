"""CRUD génériques avec invalidation de cache."""

from __future__ import annotations

from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import get_redis
from app.services.cache import ReferentialCache

ModelT = TypeVar("ModelT")


class NotFoundError(Exception):
    def __init__(self, entity: str, id_: UUID) -> None:
        self.entity = entity
        self.id = id_
        super().__init__(f"{entity} {id_} introuvable.")


class ConflictError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


async def _invalidate(entity_name: str) -> None:
    """Invalide le cache d'une entité (versioning)."""
    redis = await get_redis()
    await ReferentialCache(redis).invalidate(entity_name)
    # Invalide aussi les listes dépendantes (relations FK)
    if entity_name in ("levels", "subjects", "series"):
        await ReferentialCache(redis).invalidate("chapters")
    if entity_name in ("chapters",):
        await ReferentialCache(redis).invalidate("resources")


async def create_entity(
    session: AsyncSession,
    *,
    model: type[ModelT],
    entity_name: str,
    data: BaseModel,
) -> ModelT:
    """Crée une entité, invalide le cache, lève ConflictError si doublon."""
    obj = model(**data.model_dump(exclude_unset=True))
    session.add(obj)
    try:
        await session.flush()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError(f"Conflit d'unicité pour {entity_name}.") from exc
    await session.commit()
    await session.refresh(obj)
    await _invalidate(entity_name)
    return obj


async def update_entity(
    session: AsyncSession,
    *,
    model: type[ModelT],
    entity_name: str,
    id_: UUID,
    data: BaseModel,
) -> ModelT:
    """Met à jour partiellement une entité, invalide le cache."""
    obj = await session.get(model, id_)
    if obj is None:
        raise NotFoundError(entity_name, id_)

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)

    try:
        await session.flush()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError(f"Conflit d'unicité pour {entity_name}.") from exc
    await session.commit()
    await session.refresh(obj)
    await _invalidate(entity_name)
    return obj


async def delete_entity(
    session: AsyncSession,
    *,
    model: type[ModelT],
    entity_name: str,
    id_: UUID,
) -> None:
    """Supprime une entité, invalide le cache."""
    obj = await session.get(model, id_)
    if obj is None:
        raise NotFoundError(entity_name, id_)
    await session.delete(obj)
    try:
        await session.flush()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError(
            f"Suppression impossible : {entity_name} est référencé ailleurs."
        ) from exc
    await session.commit()
    await _invalidate(entity_name)
