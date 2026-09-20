"""Journal des événements CRDT additifs (XP, streaks).

**Propriété CRDT** : chaque événement est unique par ``(student_id, event_id)``.
L'application est **idempotente** : rejouer un événement déjà traité retourne
``deduplicated=True`` sans modifier l'état.

**Usage** : un client offline accumule des événements XP/streak dans son
``sync_outbox`` local, puis les envoie un par un à ``/sync/apply-event``.
Le serveur déduplique par ``event_id`` (généré côté client, UUID v4).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin
from app.models.enums import UserEventKind, pg_enum


class UserEvent(UUIDMixin, Base):
    """Événement CRDT additif émis par un client offline.

    Une fois inséré, un événement est **immuable** (audit trail).
    """

    __tablename__ = "user_events"
    __table_args__ = (
        UniqueConstraint(
            "student_id", "event_id", name="uq_user_events_student_event"
        ),
        Index("ix_user_events_student_kind", "student_id", "kind"),
        Index("ix_user_events_event_ts", "event_ts"),
        {"comment": "Journal CRDT additif (XP, streaks)"},
    )

    event_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        comment="UUID v4 généré par le client (déduplication)",
    )
    student_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    kind: Mapped[UserEventKind] = mapped_column(
        pg_enum(UserEventKind, "user_event_kind"),
        nullable=False,
    )
    amount: Mapped[int | None] = mapped_column(
        Integer, nullable=True,
        comment="Valeur numérique (ex: XP gagnés). NULL si non applicable.",
    )
    reason: Mapped[str | None] = mapped_column(
        String(100), nullable=True,
        comment="Raison métier (ex: 'quiz_passed', 'lesson_completed')",
    )
    event_ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Horodatage client de l'événement",
    )
    payload: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default="{}",
    )
    server_ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<UserEvent event_id={self.event_id} kind={self.kind.value}>"
