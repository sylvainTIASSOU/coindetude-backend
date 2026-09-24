"""Endpoints du profil élève.

Flow d'onboarding :
1. ``GET /students/me/profile/options`` → toutes les options (cycles/niveaux/séries).
2. ``PUT /students/me/profile`` → définit niveau + série.
3. ``GET /students/me/profile`` → relit son profil à tout moment.
4. ``POST /students/me/profile/regenerate-pairing-code`` → nouveau code parent.
5. ``GET /students/{id}/profile`` → lecture par un parent (lien requis).
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.api.deps import CurrentUser, DbSession
from app.core.logging import log as logger
from app.schemas.students import (
    ProfileOptionsResponse,
    StudentProfilePublic,
    StudentProfileRead,
    StudentProfileUpsertRequest,
)
from app.services.students.errors import StudentError
from app.services.students.service import StudentsService

router = APIRouter(prefix="/students", tags=["students"])


def _handle_error(exc: StudentError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=exc.detail)


# =============================================================================
# Options d'onboarding (public-ish, mais protégé pour usage authentifié)
# =============================================================================

@router.get(
    "/me/profile/options",
    response_model=ProfileOptionsResponse,
    summary="Options d'onboarding (cycles, niveaux, séries)",
    description=(
        "Retourne tous les cycles disponibles avec leurs niveaux et séries. "
        "Utilisé par l'écran d'onboarding élève. Caché 1h côté serveur + "
        "`Cache-Control: public, max-age=3600` pour le client."
    ),
)
async def get_profile_options(
    _user: CurrentUser,
    session: DbSession,
) -> JSONResponse:
    service = StudentsService(session)
    cycles = await service.get_profile_options()
    payload = ProfileOptionsResponse(
        cycles=cycles, cache_ttl=3600
    ).model_dump(mode="json")
    return JSONResponse(
        content=payload,
        headers={"Cache-Control": "public, max-age=3600"},
    )


# =============================================================================
# Upsert profil
# =============================================================================

@router.put(
    "/me/profile",
    response_model=StudentProfileRead,
    summary="Crée ou met à jour le profil élève (niveau + série)",
    description=(
        "Endpoint idempotent. Le client envoie le **nom** du niveau et le "
        "**code** de la série (pas les UUIDs). Le serveur résout les entités "
        "et valide la compatibilité niveau ↔ série via `level_series`.\n\n"
        "Un élève de cycle `college` ne peut pas avoir de série."
    ),
    responses={
        200: {"description": "Profil mis à jour"},
        403: {"description": "L'utilisateur n'est pas un élève"},
        404: {"description": "Niveau ou série introuvable"},
        422: {"description": "Série non autorisée pour ce niveau, ou payload invalide"},
    },
)
async def upsert_my_profile(
    payload: StudentProfileUpsertRequest,
    user: CurrentUser,
    session: DbSession,
) -> StudentProfileRead:
    service = StudentsService(session)
    try:
        return await service.upsert_profile(user=user, payload=payload)
    except StudentError as exc:
        raise _handle_error(exc) from exc


# =============================================================================
# Lecture self
# =============================================================================

@router.get(
    "/me/profile",
    response_model=StudentProfileRead,
    summary="Mon profil élève",
)
async def get_my_profile(
    user: CurrentUser,
    session: DbSession,
) -> StudentProfileRead:
    service = StudentsService(session)
    try:
        return await service.get_my_profile(user=user)
    except StudentError as exc:
        raise _handle_error(exc) from exc


# =============================================================================
# Régénération du code parent
# =============================================================================

@router.post(
    "/me/profile/regenerate-pairing-code",
    summary="Régénère le code de liaison parent",
    description=(
        "Invalide l'ancien code et en génère un nouveau à 6 caractères. "
        "À utiliser si le code a été partagé par erreur. **Les liens parents "
        "existants ne sont pas supprimés** — seul le code de liaison change."
    ),
    responses={
        200: {"description": "Nouveau code retourné"},
        403: {"description": "L'utilisateur n'est pas un élève"},
    },
)
async def regenerate_pairing_code(
    user: CurrentUser,
    session: DbSession,
) -> dict[str, str]:
    service = StudentsService(session)
    try:
        new_code = await service.regenerate_pairing_code(user=user)
    except StudentError as exc:
        raise _handle_error(exc) from exc
    return {"pairing_code": new_code}


# =============================================================================
# Lecture par un parent
# =============================================================================

@router.get(
    "/{student_id}/profile",
    response_model=StudentProfilePublic,
    summary="Profil d'un élève (parent uniquement)",
    description=(
        "Lecture du profil d'un enfant par un parent. Le lien "
        "`parent_student` doit exister. Le `pairing_code` n'est **jamais** "
        "exposé à un tiers."
    ),
    responses={
        403: {"description": "Pas de lien parent-élève"},
        404: {"description": "Profil introuvable"},
    },
)
async def get_student_profile_for_guardian(
    student_id: UUID,
    user: CurrentUser,
    session: DbSession,
) -> StudentProfilePublic:
    service = StudentsService(session)
    try:
        return await service.get_profile_for_guardian(
            guardian=user, student_id=student_id
        )
    except StudentError as exc:
        raise _handle_error(exc) from exc