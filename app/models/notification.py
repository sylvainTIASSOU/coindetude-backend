"""Modèles liés aux notifications et au push FCM."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import NotificationType, Platform, pg_enum

if TYPE_CHECKING:
    from app.models.user import User


class DeviceToken(UUIDMixin, TimestampMixin, Base):
    """Jeton FCM d'un appareil pour recevoir les push notifications."""

    __tablename__ = "device_tokens"
    __table_args__ = (
        Index("ix_device_tokens_user_id", "user_id"),
        {"comment": "Jetons FCM par appareil utilisateur"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    fcm_token: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False,
    )
    platform: Mapped[Platform] = mapped_column(
        pg_enum(Platform, "platform"),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", lazy="noload")

    def __repr__(self) -> str:
        return f"<DeviceToken id={self.id} platform={self.platform.value}>"


class NotificationPreference(TimestampMixin, Base):
    """Préférences de notification (1-1 avec User)."""

    __tablename__ = "notification_preferences"
    __table_args__ = (
        {"comment": "Préférences de notification par utilisateur"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    alerts_exam: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true",
    )
    alerts_study: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true",
    )
    alerts_news: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false",
    )

    def __repr__(self) -> str:
        return f"<NotificationPreference user_id={self.user_id}>"


class SentNotification(UUIDMixin, Base):
    """Historique des notifications envoyées (log immuable)."""

    __tablename__ = "sent_notifications"
    __table_args__ = (
        Index("ix_sent_notifications_user_id_created_at", "user_id", "created_at"),
        Index("ix_sent_notifications_is_read", "is_read"),
        {"comment": "Historique des notifications envoyées aux utilisateurs"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[NotificationType] = mapped_column(
        pg_enum(NotificationType, "notification_type"),
        nullable=False,
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    def __repr__(self) -> str:
        return f"<SentNotification id={self.id} type={self.type.value}>"