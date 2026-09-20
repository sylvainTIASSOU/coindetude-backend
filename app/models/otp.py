"""Codes OTP à usage unique pour la vérification de numéro de téléphone.

**Sécurité** :
- Code à 6 chiffres généré par CSPRNG.
- Stocké sous forme HMAC-SHA256(code, SECRET_KEY + phone + purpose).
- 5 tentatives max, TTL 5 min (register/login) ou 10 min (reset_password).
- Usage unique via ``consumed_at``.
- Purge automatique après 7 jours (job ARQ).
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin
from app.models.enums import OTPChannel, OTPPurpose, pg_enum


class OTPCode(UUIDMixin, Base):
    """Un code OTP émis pour un (phone, purpose) donné.

    Le champ ``id`` (UUID) sert de ``challenge_id`` retourné au client. Le
    client le présente à ``/verify-otp`` avec le code reçu par WhatsApp/SMS.
    """

    __tablename__ = "otp_codes"
    __table_args__ = (
        Index("ix_otp_codes_user_id", "user_id"),
        Index("ix_otp_codes_phone_purpose", "phone", "purpose"),
        Index("ix_otp_codes_expires_at", "expires_at"),
        {"comment": "Codes OTP à usage unique"},
    )

    user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        comment="NULL si le phone est inconnu (anti-énumération)",
    )
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    purpose: Mapped[OTPPurpose] = mapped_column(
        pg_enum(OTPPurpose, "otp_purpose"), nullable=False
    )
    code_hash: Mapped[str] = mapped_column(
        String(64), nullable=False,
        comment="HMAC-SHA256(code, SECRET_KEY+phone+purpose) hex",
    )
    channel: Mapped[OTPChannel] = mapped_column(
        pg_enum(OTPChannel, "otp_channel"), nullable=False
    )
    provider_message_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    attempts: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    max_attempts: Mapped[int] = mapped_column(
        Integer, nullable=False, default=5, server_default="5"
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    consumed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<OTPCode id={self.id} purpose={self.purpose.value}>"
