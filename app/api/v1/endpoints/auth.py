"""Endpoints d'authentification : inscription et connexion (JWT)."""

from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.api.deps import DbSession
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.user import CustomerSignin, RefreshTokenRequest, UserCreate, UserRead, UserSigin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: DbSession) -> User:
    existing = await db.scalar(select(User).where(User.email == (str(payload.email))))
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Email déjà utilisé")

    user = User(
        email=str(payload.email),
        full_name=payload.full_name,
        phone=payload.phone,
        role=payload.role,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login")
async def login(
    db: DbSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict[str, str]:
    user = await db.scalar(select(User).where(User.email == (str(form_data.username))))
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/signin")
async def signin(
    db: DbSession,
    payload: UserSigin,
) -> dict[str, str]:
    user = await db.scalar(select(User).where(User.email == (str(payload.email))))
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/signin-customer")
async def signin_customer(
    db: DbSession,
    payload: CustomerSignin,
) -> dict[str, str]:
    user = await db.scalar(select(User).where(User.phone == (str(payload.phone))))
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="phone ou mot de passe incorrect",
        )

    if str(user.role).lower() == "ADMIN".lower():
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Reessaiyer avec une autre compte.",
        )
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh")
async def refresh(
    db: DbSession,
    payload: RefreshTokenRequest,
):
    try:
        decoded = decode_access_token(payload.refresh_token)
    except jwt.PyJWTError:
        raise HTTPException(  # noqa: B904
            status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalide",
        )
    user_id = decoded.get("sub")
    if user_id is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalide",
        )
    user = await db.scalar(select(User).where(User.id == (user_id)))
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé",
        )
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
