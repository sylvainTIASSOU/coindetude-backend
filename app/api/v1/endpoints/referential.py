"""Endpoints publics du référentiel pédagogique.

**Caractéristiques** :
- Accessibles **sans authentification** (données publiques officielles).
- Cache Redis 1h + header ``Cache-Control: public, max-age=3600``.
- Pagination offset-based.
- Filtres simples (par cycle, level, subject, type...).
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import DbSession
from app.core.logging import log as logger
from app.db.redis import get_redis
from app.models import (
    Chapter,
    Cycle,
    Level,
    Resource,
    ResourceType,
    Series,
    Subject,
)
from app.schemas.common import PageResponse
from app.schemas.referential import (
    ChapterRead,
    LevelRead,
    ResourceRead,
    ResourceReadDetail,
    SeriesRead,
    SubjectRead,
)
from app.services.cache import ReferentialCache, cache_control_header
from app.services.storage.s3_client import get_s3_client

router = APIRouter(prefix="/referential", tags=["referential"])


async def _get_cache() -> ReferentialCache:
    redis = await get_redis()
    return ReferentialCache(redis)


async def _paginated_query(
    session: AsyncSession,
    stmt,
    *,
    limit: int,
    offset: int,
) -> tuple[list, int]:
    """Exécute une requête paginée. Retourne (items, total)."""
    total = await session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = (await session.execute(stmt.limit(limit).offset(offset))).scalars().all()
    return list(rows), total


# =============================================================================
# LEVELS
# =============================================================================


@router.get(
    "/levels",
    response_model=PageResponse[LevelRead],
    summary="Liste des niveaux scolaires",
)
async def list_levels(
    request: Request,
    session: DbSession,
    cycle: Annotated[Cycle | None, Query(description="Filtre par cycle")] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> JSONResponse:
    cache = await _get_cache()
    filters = {"cycle": cycle.value if cycle else None, "limit": limit, "offset": offset}

    cached = await cache.get("levels", filters)
    if cached:
        return JSONResponse(content=cached, headers=cache_control_header())

    stmt = select(Level).order_by(Level.order_index, Level.name)
    if cycle:
        stmt = stmt.where(Level.cycle == cycle)

    items, total = await _paginated_query(session, stmt, limit=limit, offset=offset)
    payload = PageResponse[LevelRead](
        items=[LevelRead.model_validate(x) for x in items],
        total=total,
        limit=limit,
        offset=offset,
        has_more=(offset + limit) < total,
    ).model_dump(mode="json")

    await cache.set("levels", filters, payload)
    return JSONResponse(content=payload, headers=cache_control_header())


# =============================================================================
# SERIES
# =============================================================================


@router.get(
    "/series",
    response_model=PageResponse[SeriesRead],
    summary="Liste des séries (lycée)",
)
async def list_series(
    session: DbSession,
    cycle: Annotated[Cycle | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> JSONResponse:
    cache = await _get_cache()
    filters = {"cycle": cycle.value if cycle else None, "limit": limit, "offset": offset}
    cached = await cache.get("series", filters)
    if cached:
        return JSONResponse(content=cached, headers=cache_control_header())

    stmt = select(Series).order_by(Series.cycle, Series.code)
    if cycle:
        stmt = stmt.where(Series.cycle == cycle)

    items, total = await _paginated_query(session, stmt, limit=limit, offset=offset)
    payload = PageResponse[SeriesRead](
        items=[SeriesRead.model_validate(x) for x in items],
        total=total,
        limit=limit,
        offset=offset,
        has_more=(offset + limit) < total,
    ).model_dump(mode="json")

    await cache.set("series", filters, payload)
    return JSONResponse(content=payload, headers=cache_control_header())


# =============================================================================
# SUBJECTS
# =============================================================================


@router.get(
    "/subjects",
    response_model=PageResponse[SubjectRead],
    summary="Liste des matières",
)
async def list_subjects(
    session: DbSession,
    cycle: Annotated[Cycle | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> JSONResponse:
    cache = await _get_cache()
    filters = {"cycle": cycle.value if cycle else None, "limit": limit, "offset": offset}
    cached = await cache.get("subjects", filters)
    if cached:
        return JSONResponse(content=cached, headers=cache_control_header())

    stmt = select(Subject).order_by(Subject.name)
    if cycle:
        # Matières spécifiques au cycle OU transverses (cycle NULL)
        stmt = stmt.where((Subject.cycle == cycle) | (Subject.cycle.is_(None)))

    items, total = await _paginated_query(session, stmt, limit=limit, offset=offset)
    payload = PageResponse[SubjectRead](
        items=[SubjectRead.model_validate(x) for x in items],
        total=total,
        limit=limit,
        offset=offset,
        has_more=(offset + limit) < total,
    ).model_dump(mode="json")

    await cache.set("subjects", filters, payload)
    return JSONResponse(content=payload, headers=cache_control_header())


# =============================================================================
# CHAPTERS
# =============================================================================


@router.get(
    "/chapters",
    response_model=PageResponse[ChapterRead],
    summary="Liste des chapitres",
)
async def list_chapters(
    session: DbSession,
    level_id: Annotated[UUID | None, Query()] = None,
    subject_id: Annotated[UUID | None, Query()] = None,
    series_id: Annotated[UUID | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> JSONResponse:
    cache = await _get_cache()
    filters = {
        "level_id": str(level_id) if level_id else None,
        "subject_id": str(subject_id) if subject_id else None,
        "series_id": str(series_id) if series_id else None,
        "limit": limit,
        "offset": offset,
    }
    cached = await cache.get("chapters", filters)
    if cached:
        return JSONResponse(content=cached, headers=cache_control_header())

    stmt = select(Chapter).order_by(Chapter.order_index)
    if level_id:
        stmt = stmt.where(Chapter.level_id == level_id)
    if subject_id:
        stmt = stmt.where(Chapter.subject_id == subject_id)
    if series_id:
        # Chapitres spécifiques à cette série OU transverses (NULL)
        stmt = stmt.where((Chapter.series_id == series_id) | (Chapter.series_id.is_(None)))

    items, total = await _paginated_query(session, stmt, limit=limit, offset=offset)
    payload = PageResponse[ChapterRead](
        items=[ChapterRead.model_validate(x) for x in items],
        total=total,
        limit=limit,
        offset=offset,
        has_more=(offset + limit) < total,
    ).model_dump(mode="json")

    await cache.set("chapters", filters, payload)
    return JSONResponse(content=payload, headers=cache_control_header())


# =============================================================================
# RESOURCES
# =============================================================================


@router.get(
    "/resources",
    response_model=PageResponse[ResourceRead],
    summary="Liste des ressources (sans contenu lourd)",
)
async def list_resources(
    session: DbSession,
    chapter_id: Annotated[UUID | None, Query()] = None,
    type: Annotated[ResourceType | None, Query(alias="type")] = None,
    year: Annotated[int | None, Query(ge=1980, le=2100)] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> JSONResponse:
    cache = await _get_cache()
    filters = {
        "chapter_id": str(chapter_id) if chapter_id else None,
        "type": type.value if type else None,
        "year": year,
        "limit": limit,
        "offset": offset,
    }
    cached = await cache.get("resources", filters)
    if cached:
        return JSONResponse(content=cached, headers=cache_control_header())

    stmt = select(Resource).order_by(
        Resource.year.desc().nulls_last(),
        Resource.title,
    )
    if chapter_id:
        stmt = stmt.where(Resource.chapter_id == chapter_id)
    if type:
        stmt = stmt.where(Resource.type == type)
    if year:
        stmt = stmt.where(Resource.year == year)

    items, total = await _paginated_query(session, stmt, limit=limit, offset=offset)
    payload = PageResponse[ResourceRead](
        items=[ResourceRead.model_validate(x) for x in items],
        total=total,
        limit=limit,
        offset=offset,
        has_more=(offset + limit) < total,
    ).model_dump(mode="json")

    await cache.set("resources", filters, payload)
    return JSONResponse(content=payload, headers=cache_control_header())


@router.get(
    "/resources/{resource_id}",
    response_model=ResourceReadDetail,
    summary="Détail d'une ressource (avec contenu + URL fichier)",
)
async def get_resource(
    resource_id: UUID,
    session: DbSession,
) -> JSONResponse:
    cache = await _get_cache()
    filters = {"resource_id": str(resource_id)}
    cached = await cache.get("resource_detail", filters)
    if cached:
        return JSONResponse(content=cached, headers=cache_control_header())

    resource = await session.get(Resource, resource_id)
    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ressource introuvable.",
        )

    # Générer une URL presign si un fichier est attaché
    file_url: str | None = None
    if resource.file_id is not None:
        from app.models import FileStatus, StoredFile

        stored = await session.get(StoredFile, resource.file_id)
        if stored and stored.status is FileStatus.UPLOADED:
            try:
                s3 = get_s3_client()
                file_url = await s3.presign_get(key=stored.file_path)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Presign échoué pour resource=%s : %s", resource_id, exc)

    detail = ResourceReadDetail(
        id=resource.id,
        chapter_id=resource.chapter_id,
        type=resource.type,
        title=resource.title,
        file_id=resource.file_id,
        year=resource.year,
        origin=resource.origin,
        content_text=resource.content_text,
        file_url=file_url,
    )
    payload = detail.model_dump(mode="json")
    await cache.set("resource_detail", filters, payload)
    return JSONResponse(content=payload, headers=cache_control_header())
