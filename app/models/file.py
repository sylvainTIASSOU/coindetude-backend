"""Modèle des fichiers uploadés (avatars, PDF, scans IA)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import FileContext, FileStatus, pg_enum

if TYPE_CHECKING:
    from app.models.user import User


class StoredFile(UUIDMixin, TimestampMixin, Base):
    """Fichier uploadé et stocké sur le cloud.

    Cycle de vie :
    ``pending`` → (upload S3 + confirm) → ``uploaded``
    ``pending`` → (job ARQ > 24h) → supprimé (orphelin)
    """

    __tablename__ = "stored_files"
    __table_args__ = (
        UniqueConstraint("file_path", name="uq_stored_files_file_path"),
        Index("ix_stored_files_uploader_id", "uploader_id"),
        Index("ix_stored_files_context", "context"),
        Index("ix_stored_files_status_expires", "status", "expires_at"),
        {"comment": "Fichiers uploadés (avatars, PDF, scans IA)"},
    )

    uploader_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="NULL si fichier système",
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
        comment="Clé objet sur S3/MinIO/R2 (ex: avatars/{user_id}/{file_id}.webp)",
    )
    mime_type: Mapped[str] = mapped_column(String(50), nullable=False)
    context: Mapped[FileContext] = mapped_column(
        pg_enum(FileContext, "file_context"),
        nullable=False,
    )
    status: Mapped[FileStatus] = mapped_column(
        pg_enum(FileStatus, "file_status"),
        nullable=False,
        default=FileStatus.PENDING,
        server_default=FileStatus.PENDING.value,
    )
    size_kb_declared: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Taille annoncée par le client au presign",
    )
    size_kb_actual: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Taille réelle mesurée à la confirmation (head_object)",
    )
    uploaded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Pour les fichiers pending : date d'expiration (purge ARQ)",
    )

    # Relations
    uploader: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[uploader_id],
        lazy="noload",
    )

    @property
    def is_ready(self) -> bool:
        return self.status is FileStatus.UPLOADED

    def __repr__(self) -> str:
        return f"<StoredFile id={self.id} status={self.status.value}>"
