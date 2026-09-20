"""Appareils de confiance (option "Se souvenir de moi" sur 30 jours).

Lors d'un ``/verify-otp`` avec ``remember_device=true``, un token opaque
est émis et stocké en base (hash SHA-256). Les ``/login`` suivants depuis
ce device peuvent skip l'OTP en présentant ce token dans le header
``X-Trusted-Device``.

Sécurité :
- Token opaque (32 octets urlsafe), jamais en clair en base.
- TTL 30 jours, prolongé à chaque usage (``last_used_at``).
- Révocable via ``/logout-all`` ou par expiration.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class TrustedDevice(UUIDMixin, Base):
    """Appareil de confiance d'un utilisateur."""

    __tablename__ = "trusted_devices"
    __table_args__ = (
        UniqueConstraint("token_hash", name="uq_trusted_devices_token_hash"),
        Index("ix_trusted_devices_user_id", "user_id"),
        Index("ix_trusted_devices_expires_at", "expires_at"),
        {"comment": "Appareils de confiance (skip OTP pendant 30j)"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    token_hash: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True,
        comment="SHA-256 du token trusted device (jamais en clair)",
    )
    device_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    last_used_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    @property
    def is_valid(self) -> bool:
        from app.core.security import utcnow # type: ignore
        return self.expires_at > utcnow() # type: ignore

    def __repr__(self) -> str:
        return f"<TrustedDevice user={self.user_id} id={self.id}>"
