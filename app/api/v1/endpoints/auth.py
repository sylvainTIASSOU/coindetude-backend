"""Endpoints d'authentification avec OTP.

Flow :
1. POST /auth/register    → 202 OTPSentResponse
2. POST /auth/verify-otp  → 200 AuthResponse (register/login)
3. POST /auth/login       → 202 OTPSentResponse OU 200 AuthResponse (trusted)
4. POST /auth/forgot-password → 202 OTPSentResponse
5. POST /auth/reset-password  → 200 AuthResponse
6. POST /auth/resend-otp  → 202 OTPSentResponse
7. POST /auth/refresh     → 200 TokenPair
8. POST /auth/logout      → 204
9. POST /auth/logout-all  → 204
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Body, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.api.deps import CurrentUser, DbSession
from app.db.redis import get_redis
from app.schemas.auth import (
    AuthResponse,
    ForgotPasswordRequest,
    LoginRequest,
    OTPSentResponse,
    RefreshRequest,
    RegisterRequest,
    ResendOTPRequest,
    ResetPasswordRequest,
    TokenPair,
    UserRead,
    VerifyOTPRequest,
)
from app.services.auth_service import (
    AuthResult,
    AuthService,
    AuthServiceError,
    OTPSent,
)
from app.services.otp.rate_limiter import RateLimitExceeded
from app.services.otp.service import (
    OTPExpired,
    OTPInvalid,
    OTPTooManyAttempts,
)
from app.services.token_service import (
    TokenExpired,
    TokenInvalid,
    TokenReuseDetected,
    get_token_service,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _client_meta(request: Request) -> dict[str, str | None]:
    ua = request.headers.get("user-agent")
    forwarded = request.headers.get("x-forwarded-for")
    ip = (
        forwarded.split(",")[0].strip()
        if forwarded
        else (request.client.host if request.client else None)
    )
    return {"user_agent": ua, "ip_address": ip}


async def _get_auth_service(session) -> AuthService: # type: ignore
    redis = await get_redis()
    return AuthService(session, redis) # type: ignore


def _otp_response(otp_sent: OTPSent) -> OTPSentResponse:
    return OTPSentResponse(
        challenge_id=otp_sent.challenge_id,
        expires_in=otp_sent.expires_in,
        channel=otp_sent.channel,
        masked_phone=otp_sent.masked_phone,
        dev_code=otp_sent.dev_code,
    )


def _auth_response(result: AuthResult) -> AuthResponse:
    return AuthResponse(
        access_token=result.tokens.access_token,
        refresh_token=result.tokens.refresh_token,
        expires_in=result.tokens.expires_in,
        user=UserRead.model_validate(result.user),
        trusted_device_token=result.trusted_device_token,
    )


def _handle_service_error(exc: AuthServiceError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=exc.detail)


# =====================================================================
# ÉTAPE 1
# =====================================================================


@router.post(
    "/register",
    response_model=OTPSentResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Étape 1 — Inscription : envoie un OTP",
)
async def register(
    payload: RegisterRequest,
    request: Request,
    session: DbSession,
) -> OTPSentResponse:
    svc = await _get_auth_service(session)
    meta = _client_meta(request)
    try:
        otp_sent = await svc.register(
            first_name=payload.first_name,
            last_name=payload.last_name,
            phone=payload.phone,
            email=payload.email,
            password=payload.password,
            role=payload.role,
            ip_address=meta["ip_address"],
            user_agent=meta["user_agent"],
        )
    except AuthServiceError as exc:
        raise _handle_service_error(exc) from exc
    except RateLimitExceeded as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
            headers={"Retry-After": str(exc.retry_after)},
        ) from exc
    await session.commit()
    return _otp_response(otp_sent)


@router.post(
    "/login",
    summary="Étape 1 — Login : envoie un OTP (ou skip si device de confiance)",
)
async def login(
    payload: LoginRequest,
    request: Request,
    session: DbSession,
    x_trusted_device: Annotated[str | None, Header(alias="X-Trusted-Device")] = None,
) -> Any:
    svc = await _get_auth_service(session)
    meta = _client_meta(request)
    try:
        result = await svc.login(
            phone=payload.phone,
            password=payload.password,
            ip_address=meta["ip_address"],
            user_agent=meta["user_agent"],
            trusted_device_token=x_trusted_device,
        )
    except AuthServiceError as exc:
        raise _handle_service_error(exc) from exc
    except RateLimitExceeded as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
            headers={"Retry-After": str(exc.retry_after)},
        ) from exc
    await session.commit()

    if isinstance(result, AuthResult):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=_auth_response(result).model_dump(mode="json"),
        )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=_otp_response(result).model_dump(mode="json"),
    )


@router.post(
    "/forgot-password",
    response_model=OTPSentResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def forgot_password(
    payload: ForgotPasswordRequest,
    request: Request,
    session: DbSession,
) -> OTPSentResponse:
    svc = await _get_auth_service(session)
    meta = _client_meta(request)
    try:
        otp_sent = await svc.forgot_password(
            phone=payload.phone,
            ip_address=meta["ip_address"],
            user_agent=meta["user_agent"],
        )
    except RateLimitExceeded as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
            headers={"Retry-After": str(exc.retry_after)},
        ) from exc
    await session.commit()
    return _otp_response(otp_sent)


@router.post(
    "/resend-otp",
    response_model=OTPSentResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def resend_otp(
    payload: ResendOTPRequest,
    request: Request,
    session: DbSession,
) -> OTPSentResponse:
    svc = await _get_auth_service(session)
    meta = _client_meta(request)
    try:
        otp_sent = await svc.resend_otp(
            challenge_id=payload.challenge_id,
            ip_address=meta["ip_address"],
            user_agent=meta["user_agent"],
        )
    except AuthServiceError as exc:
        raise _handle_service_error(exc) from exc
    except RateLimitExceeded as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
            headers={"Retry-After": str(exc.retry_after)},
        ) from exc
    await session.commit()
    return _otp_response(otp_sent)


# =====================================================================
# ÉTAPE 2
# =====================================================================


@router.post(
    "/verify-otp",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_otp(
    payload: VerifyOTPRequest,
    request: Request,
    session: DbSession,
) -> AuthResponse:
    svc = await _get_auth_service(session)
    meta = _client_meta(request)
    try:
        result = await svc.verify_otp(
            challenge_id=payload.challenge_id,
            code=payload.code,
            remember_device=payload.remember_device,
            user_agent=meta["user_agent"],
            ip_address=meta["ip_address"],
        )
    except OTPExpired as exc:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=str(exc)) from exc
    except OTPInvalid as exc:
        await session.commit()  # persiste le compteur attempts
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    except OTPTooManyAttempts as exc:
        await session.commit()
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc)) from exc
    except AuthServiceError as exc:
        raise _handle_service_error(exc) from exc

    await session.commit()
    return _auth_response(result)


@router.post(
    "/reset-password",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
)
async def reset_password(
    payload: ResetPasswordRequest,
    request: Request,
    session: DbSession,
) -> AuthResponse:
    svc = await _get_auth_service(session)
    meta = _client_meta(request)
    try:
        result = await svc.reset_password(
            challenge_id=payload.challenge_id,
            code=payload.code,
            new_password=payload.new_password,
            user_agent=meta["user_agent"],
            ip_address=meta["ip_address"],
        )
    except OTPExpired as exc:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=str(exc)) from exc
    except OTPInvalid as exc:
        await session.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    except OTPTooManyAttempts as exc:
        await session.commit()
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc)) from exc
    except AuthServiceError as exc:
        raise _handle_service_error(exc) from exc
    await session.commit()
    return _auth_response(result)


# =====================================================================
# Refresh / Logout (inchangés)
# =====================================================================


@router.post("/refresh", response_model=TokenPair)
async def refresh(
    request: Request,
    session: DbSession,
    payload: Annotated[RefreshRequest | None, Body()] = None,
    x_refresh_token: Annotated[str | None, Header(alias="X-Refresh-Token")] = None,
) -> TokenPair:
    presented = (payload.refresh_token if payload else None) or x_refresh_token
    if not presented:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="refresh_token requis (body ou header X-Refresh-Token).",
        )

    svc = await get_token_service(session)
    try:
        issued = await svc.rotate(presented_token=presented, **_client_meta(request))
    except (TokenInvalid, TokenExpired) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    except TokenReuseDetected as exc:
        await session.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"X-Token-Reuse-Detected": "1"},
        ) from exc
    await session.commit()
    return TokenPair(
        access_token=issued.access_token,
        refresh_token=issued.refresh_token,
        expires_in=issued.expires_in,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    session: DbSession,
    _user: CurrentUser,
    payload: Annotated[RefreshRequest | None, Body()] = None,
    x_refresh_token: Annotated[str | None, Header(alias="X-Refresh-Token")] = None,
) -> None:
    presented = (payload.refresh_token if payload else None) or x_refresh_token
    if not presented:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="refresh_token requis.",
        )
    svc = await get_token_service(session)
    await svc.revoke_token(presented)
    await session.commit()


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(session: DbSession, user: CurrentUser) -> None:
    svc = await get_token_service(session)
    await svc.revoke_all_user_tokens(user.id)
    # Révoquer aussi tous les trusted devices
    from app.services.trusted_device_service import TrustedDeviceService

    await TrustedDeviceService(session).revoke_all_for_user(user.id)
    await session.commit()
