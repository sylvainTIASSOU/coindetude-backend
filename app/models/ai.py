"""Modèles du Tuteur IA : conversations, messages, fiches générées."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import AIRole, pg_enum

if TYPE_CHECKING:
    from app.models.user import User


class AIConversation(UUIDMixin, TimestampMixin, Base):
    """Session de chat entre un élève et le Tuteur IA."""

    __tablename__ = "ai_conversations"
    __table_args__ = (
        Index("ix_ai_conversations_student_id", "student_id"),
        Index("ix_ai_conversations_chapter_id", "chapter_id"),
        {"comment": "Sessions de chat avec le Tuteur IA"},
    )

    student_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    chapter_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("chapters.id", ondelete="SET NULL"),
        nullable=True,
        comment="Contexte pédagogique optionnel",
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    student: Mapped["User"] = relationship("User", lazy="noload")
    messages: Mapped[list["AIMessage"]] = relationship(
        "AIMessage",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="AIMessage.created_at",
        lazy="noload",
    )

    def __repr__(self) -> str:
        return f"<AIConversation id={self.id} title={self.title}>"


class AIMessage(UUIDMixin, Base):
    """Message individuel d'une conversation IA (immuable)."""

    __tablename__ = "ai_messages"
    __table_args__ = (
        Index("ix_ai_messages_conversation_id_created_at", "conversation_id", "created_at"),
        {"comment": "Messages des conversations IA (user/assistant/system)"},
    )

    conversation_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai_conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[AIRole] = mapped_column(
        pg_enum(AIRole, "ai_role"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    file_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("stored_files.id", ondelete="SET NULL"),
        nullable=True,
        comment="Photo de cahier scannée jointe au message",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    conversation: Mapped[AIConversation] = relationship(
        "AIConversation",
        back_populates="messages",
    )

    def __repr__(self) -> str:
        return f"<AIMessage id={self.id} role={self.role.value}>"


class StudyFiche(UUIDMixin, TimestampMixin, Base):
    """Fiche de synthèse générée par l'IA pour un élève.

    Le contenu est structuré en JSONB pour permettre un rendu typé côté Flutter :
    ``{"definitions": [...], "formules": [...], "erreurs_frequentes": [...]}``.
    """

    __tablename__ = "study_fiches"
    __table_args__ = (
        Index("ix_study_fiches_student_id", "student_id"),
        Index("ix_study_fiches_chapter_id", "chapter_id"),
        {"comment": "Fiches de synthèse générées par l'IA"},
    )

    student_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    chapter_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("chapters.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False,
        comment="Structure : definitions / formules / erreurs_frequentes / resume",
    )
    source_file_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("stored_files.id", ondelete="SET NULL"),
        nullable=True,
        comment="Photo du cahier source",
    )

    student: Mapped["User"] = relationship("User", lazy="noload")

    def __repr__(self) -> str:
        return f"<StudyFiche id={self.id} title={self.title}>"