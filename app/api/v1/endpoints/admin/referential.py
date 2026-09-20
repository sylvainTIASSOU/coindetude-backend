"""Endpoints CRUD admin pour le référentiel pédagogique.

Tous les endpoints requièrent ``role == admin``.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps import AdminUser, DbSession
from app.models import Chapter, Level, Resource, Series, Subject
from app.schemas.referential import (
    ChapterCreate,
    ChapterRead,
    ChapterUpdate,
    LevelCreate,
    LevelRead,
    LevelUpdate,
    ResourceCreate,
    ResourceRead,
    ResourceUpdate,
    SeriesCreate,
    SeriesRead,
    SeriesUpdate,
    SubjectCreate,
    SubjectRead,
    SubjectUpdate,
)
from app.services.referential.crud import (
    ConflictError,
    NotFoundError,
    create_entity,
    delete_entity,
    update_entity,
)

router = APIRouter(prefix="/admin/referential", tags=["admin:referential"])


def _handle_error(exc: Exception) -> HTTPException:
    if isinstance(exc, NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, ConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail)
    return HTTPException(status_code=500, detail="Erreur interne.")


# =============================================================================
# LEVELS
# =============================================================================


@router.post(
    "/levels",
    response_model=LevelRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crée un niveau scolaire",
)
async def create_level(payload: LevelCreate, _admin: AdminUser, session: DbSession) -> LevelRead:
    try:
        obj = await create_entity(session, model=Level, entity_name="levels", data=payload)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
    return LevelRead.model_validate(obj)


@router.put(
    "/levels/{id_}",
    response_model=LevelRead,
    summary="Met à jour un niveau scolaire",
)
async def update_level(
    id_: UUID, payload: LevelUpdate, _admin: AdminUser, session: DbSession
) -> LevelRead:
    try:
        obj = await update_entity(session, model=Level, entity_name="levels", id_=id_, data=payload)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
    return LevelRead.model_validate(obj)


@router.delete(
    "/levels/{id_}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprime un niveau scolaire",
)
async def delete_level(id_: UUID, _admin: AdminUser, session: DbSession) -> None:
    try:
        await delete_entity(session, model=Level, entity_name="levels", id_=id_)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc


# =============================================================================
# SERIES
# =============================================================================


@router.post(
    "/series",
    response_model=SeriesRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_series(payload: SeriesCreate, _admin: AdminUser, session: DbSession) -> SeriesRead:
    try:
        obj = await create_entity(session, model=Series, entity_name="series", data=payload)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
    return SeriesRead.model_validate(obj)


@router.put("/series/{id_}", response_model=SeriesRead)
async def update_series(
    id_: UUID, payload: SeriesUpdate, _admin: AdminUser, session: DbSession
) -> SeriesRead:
    try:
        obj = await update_entity(
            session, model=Series, entity_name="series", id_=id_, data=payload
        )
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
    return SeriesRead.model_validate(obj)


@router.delete("/series/{id_}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_series(id_: UUID, _admin: AdminUser, session: DbSession) -> None:
    try:
        await delete_entity(session, model=Series, entity_name="series", id_=id_)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc


# =============================================================================
# SUBJECTS
# =============================================================================


@router.post(
    "/subjects",
    response_model=SubjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_subject(
    payload: SubjectCreate, _admin: AdminUser, session: DbSession
) -> SubjectRead:
    try:
        obj = await create_entity(session, model=Subject, entity_name="subjects", data=payload)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
    return SubjectRead.model_validate(obj)


@router.put("/subjects/{id_}", response_model=SubjectRead)
async def update_subject(
    id_: UUID, payload: SubjectUpdate, _admin: AdminUser, session: DbSession
) -> SubjectRead:
    try:
        obj = await update_entity(
            session, model=Subject, entity_name="subjects", id_=id_, data=payload
        )
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
    return SubjectRead.model_validate(obj)


@router.delete("/subjects/{id_}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(id_: UUID, _admin: AdminUser, session: DbSession) -> None:
    try:
        await delete_entity(session, model=Subject, entity_name="subjects", id_=id_)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc


# =============================================================================
# CHAPTERS
# =============================================================================


@router.post(
    "/chapters",
    response_model=ChapterRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_chapter(
    payload: ChapterCreate, _admin: AdminUser, session: DbSession
) -> ChapterRead:
    try:
        obj = await create_entity(session, model=Chapter, entity_name="chapters", data=payload)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
    return ChapterRead.model_validate(obj)


@router.put("/chapters/{id_}", response_model=ChapterRead)
async def update_chapter(
    id_: UUID, payload: ChapterUpdate, _admin: AdminUser, session: DbSession
) -> ChapterRead:
    try:
        obj = await update_entity(
            session, model=Chapter, entity_name="chapters", id_=id_, data=payload
        )
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
    return ChapterRead.model_validate(obj)


@router.delete("/chapters/{id_}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chapter(id_: UUID, _admin: AdminUser, session: DbSession) -> None:
    try:
        await delete_entity(session, model=Chapter, entity_name="chapters", id_=id_)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc


# =============================================================================
# RESOURCES
# =============================================================================


@router.post(
    "/resources",
    response_model=ResourceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_resource(
    payload: ResourceCreate, _admin: AdminUser, session: DbSession
) -> ResourceRead:
    try:
        obj = await create_entity(session, model=Resource, entity_name="resources", data=payload)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
    return ResourceRead.model_validate(obj)


@router.put("/resources/{id_}", response_model=ResourceRead)
async def update_resource(
    id_: UUID, payload: ResourceUpdate, _admin: AdminUser, session: DbSession
) -> ResourceRead:
    try:
        obj = await update_entity(
            session, model=Resource, entity_name="resources", id_=id_, data=payload
        )
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
    return ResourceRead.model_validate(obj)


@router.delete("/resources/{id_}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(id_: UUID, _admin: AdminUser, session: DbSession) -> None:
    try:
        await delete_entity(session, model=Resource, entity_name="resources", id_=id_)
    except (NotFoundError, ConflictError) as exc:
        raise _handle_error(exc) from exc
