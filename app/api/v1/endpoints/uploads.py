"""Endpoints /uploads : presign + confirm.

Contrat :
- ``POST /api/v1/uploads/presign``      → URL PUT pré-signée
- ``POST /api/v1/uploads/{file_id}/confirm`` → validation + URL GET

**Frugalité** : aucun contenu binaire ne transite par FastAPI. Le client
upload directement vers S3/MinIO/R2.
"""

from __future__ import annotations

import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.uploads import (
    ConfirmResponse,
    PresignRequest,
    PresignResponse,
)
from app.services.storage.uploads.errors import UploadError
from app.services.storage.uploads.service import UploadsService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post(
    "/presign",
    response_model=PresignResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Génère une URL PUT pré-signée pour upload direct",
)
async def presign(
    payload: PresignRequest,
    user: CurrentUser,
    session: DbSession,
) -> PresignResponse:
    service = UploadsService(session)
    try:
        result = await service.presign(
            user_id=user.id,
            file_name=payload.file_name,
            file_type=payload.file_type,
            size_kb=payload.size_kb,
            purpose=payload.purpose,
        )
    except UploadError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=exc.status_code, detail=exc.detail
        ) from exc

    await session.commit()
    return PresignResponse(**result)


@router.post(
    "/{file_id}/confirm",
    response_model=ConfirmResponse,
    summary="Confirme l'upload et valide le fichier côté serveur",
)
async def confirm(
    file_id: UUID,
    user: CurrentUser,
    session: DbSession,
) -> ConfirmResponse:
    service = UploadsService(session)
    try:
        result = await service.confirm(user_id=user.id, file_id=file_id)
    except UploadError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=exc.status_code, detail=exc.detail
        ) from exc

    await session.commit()
    return ConfirmResponse(**result)
