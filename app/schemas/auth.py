"""Schémas Pydantic pour les flows d'authentification OTP."""

from __future__ import annotations

import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models import OTPChannel, UserRole

_PHONE_RE = re.compile(r"^\+\d{6,15}$")
_CODE_RE = re.compile(r"^\d{6}$")


class _PhoneMixin(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def _v_phone(cls, v: str) -> str:
        v = v.strip().replace(" ", "")
        if not _PHONE_RE.match(v):
            raise ValueError("Téléphone au format international requis (+228...)")
        return v


class RegisterRequest(_PhoneMixin):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr | None = None
    password: str = Field(..., min_length=8, max_length=128)
    role: UserRole = UserRole.STUDENT

    @field_validator("password")
    @classmethod
    def _v_pwd(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")
        if not any(c.isalpha() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins une lettre")
        return v


class LoginRequest(_PhoneMixin):
    password: str


class VerifyOTPRequest(BaseModel):
    challenge_id: UUID
    code: str = Field(..., min_length=6, max_length=6)
    remember_device: bool = False

    @field_validator("code")
    @classmethod
    def _v_code(cls, v: str) -> str:
        if not _CODE_RE.match(v):
            raise ValueError("Le code doit contenir 6 chiffres")
        return v


class ResendOTPRequest(BaseModel):
    challenge_id: UUID


class ForgotPasswordRequest(_PhoneMixin):
    pass


class ResetPasswordRequest(BaseModel):
    challenge_id: UUID
    code: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def _v_pwd(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")
        if not any(c.isalpha() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins une lettre")
        return v


# --- Sorties ---


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    first_name: str
    last_name: str
    phone: str
    email: str | None
    role: UserRole
    is_active: bool
    phone_verified_at: datetime | None = None


class OTPSentResponse(BaseModel):
    """Réponse des étapes 1 (register, login, forgot, resend)."""

    challenge_id: UUID
    expires_in: int
    channel: OTPChannel
    masked_phone: str
    dev_code: str | None = Field(
        default=None,
        description="Uniquement en dev — code OTP en clair",
    )


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # noqa: S105
    expires_in: int


class AuthResponse(TokenPair):
    user: UserRead
    trusted_device_token: str | None = Field(
        default=None,
        description="Présent si remember_device=true. À stocker côté client.",
    )


class RefreshRequest(BaseModel):
    """Demande de rotation de refresh token."""

    refresh_token: str = Field(..., min_length=20)
