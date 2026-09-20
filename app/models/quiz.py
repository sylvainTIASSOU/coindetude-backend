"""Modèles des quiz d'entraînement et de leurs tentatives."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User


class Quiz(UUIDMixin, TimestampMixin, Base):
    """Quiz généré par l'IA pour un élève."""

    __tablename__ = "quizzes"
    __table_args__ = (
        Index("ix_quizzes_student_id", "student_id"),
        Index("ix_quizzes_chapter_id", "chapter_id"),
        {"comment": "Quiz d'entraînement générés par l'IA"},
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

    questions: Mapped[list["QuizQuestion"]] = relationship(
        "QuizQuestion",
        back_populates="quiz",
        cascade="all, delete-orphan",
        order_by="QuizQuestion.order_index",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Quiz id={self.id} title={self.title}>"


class QuizQuestion(UUIDMixin, TimestampMixin, Base):
    """Question individuelle d'un quiz."""

    __tablename__ = "quiz_questions"
    __table_args__ = (
        Index("ix_quiz_questions_quiz_id", "quiz_id"),
        {"comment": "Questions des quiz (QCM, Vrai/Faux, texte à trous)"},
    )

    quiz_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False,
        comment='Liste JSON des options, ex: ["1", "2", "3"]',
    )
    correct_answer: Mapped[str] = mapped_column(String(255), nullable=False)
    explanation: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="Explication IA en cas d'erreur",
    )

    quiz: Mapped[Quiz] = relationship("Quiz", back_populates="questions")

    def __repr__(self) -> str:
        return f"<QuizQuestion id={self.id} order={self.order_index}>"


class QuizAttempt(UUIDMixin, Base):
    """Tentative d'un élève sur un quiz (log immuable)."""

    __tablename__ = "quiz_attempts"
    __table_args__ = (
        Index("ix_quiz_attempts_student_id", "student_id"),
        Index("ix_quiz_attempts_quiz_id", "quiz_id"),
        {"comment": "Historique des tentatives de quiz"},
    )

    student_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    quiz_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    def __repr__(self) -> str:
        return f"<QuizAttempt id={self.id} score={self.score}/{self.total}>"