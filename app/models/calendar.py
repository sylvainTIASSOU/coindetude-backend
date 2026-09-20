"""Modèles du planning personnel et du calendrier national togolais."""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import (
    CalendarEventType,
    PlanningEventType,
    pg_enum,
)

if TYPE_CHECKING:
    from app.models.user import User


class StudyPlanning(UUIDMixin, TimestampMixin, Base):
    """Tâche de révision planifiée par un élève."""

    __tablename__ = "study_plannings"
    __table_args__ = (
        Index("ix_study_plannings_student_id_scheduled_date", "student_id", "scheduled_date"),
        Index("ix_study_plannings_is_completed", "is_completed"),
        {"comment": "Planning de révision personnel des élèves"},
    )

    student_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    event_type: Mapped[PlanningEventType] = mapped_column(
        pg_enum(PlanningEventType, "planning_event_type"),
        nullable=False,
    )
    scheduled_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false",
    )

    student: Mapped["User"] = relationship("User", lazy="noload")

    def __repr__(self) -> str:
        return f"<StudyPlanning id={self.id} title={self.title}>"


class NationalCalendar(UUIDMixin, TimestampMixin, Base):
    """Événement officiel du calendrier scolaire togolais.

    Géré par l'admin (TKMS). Cachable dans Redis pour absorber les pics
    (jour des résultats du BAC).
    """

    __tablename__ = "national_calendar"
    __table_args__ = (
        Index("ix_national_calendar_start_date", "start_date"),
        Index("ix_national_calendar_event_type", "event_type"),
        {"comment": "Calendrier scolaire officiel du Togo"},
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    event_type: Mapped[CalendarEventType] = mapped_column(
        pg_enum(CalendarEventType, "calendar_event_type"),
        nullable=False,
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(
        Date, nullable=True,
        comment="NULL pour les événements d'un seul jour",
    )

    def __repr__(self) -> str:
        return f"<NationalCalendar title={self.title} start={self.start_date}>"