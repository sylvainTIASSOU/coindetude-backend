"""Endpoint de synchronisation offline-first."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.api.deps import CurrentUser, DbSession
from app.db.redis import get_redis
from app.schemas.sync import SyncEventRequest
from app.services.sync.errors import (
    ClientTimestampOutOfWindow,
    IdempotencyInFlight,
    IdempotencyKeyConflict,
    SyncError,
)
from app.services.sync.service import SyncService

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post(
    "/apply-event",
    summary="Synchronise une mutation offline (idempotent)",
    responses={
        200: {"description": "Événement appliqué (ou replay idempotent)"},
        201: {"description": "Événement créé"},
        409: {"description": "Conflit ou clé d'idempotence réutilisée"},
        422: {"description": "Payload invalide ou client_ts hors fenêtre"},
    },
)
async def apply_event(
    payload: SyncEventRequest,
    request: Request,
    user: CurrentUser,
    session: DbSession,
    idempotency_key: Annotated[
        str,
        Header(
            alias="Idempotency-Key",
            description="UUID v4 obligatoire. Même clé + même body = même réponse.",
            min_length=8,
            max_length=64,
        ),
    ],
) -> JSONResponse:
    """Applique un événement offline avec idempotence stricte."""
    redis = await get_redis()
    service = SyncService(session, redis)

    try:
        status_code, body, is_replay = await service.apply_event(
            user_id=user.id,
            idempotency_key=idempotency_key,
            entity_type=payload.entity_type,
            operation=payload.operation,
            payload=payload.payload,
            client_ts=payload.client_ts,
        )
    except ClientTimestampOutOfWindow as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.detail,
        ) from exc
    except IdempotencyKeyConflict as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail,
            headers={"X-Idempotency-Conflict": "1"},
        ) from exc
    except IdempotencyInFlight as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail,
            headers={"Retry-After": str(exc.retry_after)},
        ) from exc
    except SyncError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    # Commit atomique : opération + clé d'idempotence
    await session.commit()

    headers: dict[str, str] = {}
    if is_replay:
        headers["X-Idempotent-Replay"] = "1"

    return JSONResponse(status_code=status_code, content=body, headers=headers)
