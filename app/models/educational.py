"""Modèles pédagogiques : niveaux, séries, matières, chapitres.

Conforme au système éducatif togolais :

- **Collège** : 6ème → 3ème, pas de séries.
- **Lycée Moderne** : 2nde, 1ère, Terminale — séries générales (A4, C, D, E...).
- **Lycée Technique** : 2nde, 1ère, Terminale — séries techniques (F1, F2, F3, F4...).

Les séries sont modélisées dans une table dédiée ``series`` avec une
association many-to-many vers ``levels`` (``level_series``) pour refléter
le fait qu'une même série peut exister sur plusieurs niveaux, et qu'un
même niveau peut proposer plusieurs séries.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import Cycle, pg_enum

if TYPE_CHECKING:
    pass


class Level(UUIDMixin, TimestampMixin, Base):
    """Niveau scolaire togolais.

    Exemples :
    - ``6ème`` (cycle ``college``)
    - ``Terminale`` (cycle ``lycee_moderne``)
    - ``1ère`` (cycle ``lycee_technique``)

    ⚠️ Un même nom de niveau (ex: "Terminale") peut exister dans plusieurs
    cycles. C'est pourquoi l'unicité porte sur ``(name, cycle)``.
    """

    __tablename__ = "levels"
    __table_args__ = (
        UniqueConstraint("name", "cycle", name="uq_levels_name_cycle"),
        Index("ix_levels_cycle", "cycle"),
        {"comment": "Niveaux scolaires (collège, lycée moderne, lycée technique)"},
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Nom du niveau (ex: 6ème, 2nde, Terminale)",
    )
    cycle: Mapped[Cycle] = mapped_column(
        pg_enum(Cycle, "cycle"),
        nullable=False,
    )
    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        comment="Ordre dans la scolarité (6ème=1, Terminale=7)",
    )

    # --- Relations ---
    chapters: Mapped[list["Chapter"]] = relationship(
        "Chapter",
        back_populates="level",
        cascade="all, delete-orphan",
        lazy="noload",
    )
    series_associations: Mapped[list["LevelSeries"]] = relationship(
        "LevelSeries",
        back_populates="level",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Level name={self.name} cycle={self.cycle.value}>"


class Series(UUIDMixin, TimestampMixin, Base):
    """Série du lycée (générale ou technique).

    Exemples :
    - ``A4`` : série littéraire (lycée moderne)
    - ``C`` : série mathématiques/physique (lycée moderne)
    - ``D`` : série mathématiques/sciences naturelles (lycée moderne)
    - ``F1`` : série mécanique (lycée technique)
    - ``F2`` : série électronique (lycée technique)

    ⚠️ Le ``cycle`` d'une série doit correspondre à celui des niveaux auxquels
    elle est associée. Cette cohérence est assurée par la logique applicative
    (validation Pydantic à la création) — pas par une contrainte SQL, car
    PostgreSQL ne peut pas exprimer une contrainte inter-table sans trigger.
    """

    __tablename__ = "series"
    __table_args__ = (
        UniqueConstraint("code", "cycle", name="uq_series_code_cycle"),
        Index("ix_series_cycle", "cycle"),
        {"comment": "Séries du lycée togolais (générales et techniques)"},
    )

    code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Code officiel de la série (ex: A4, C, D, F1)",
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment="Libellé complet (ex: 'Série A4 - Littéraire')",
    )
    cycle: Mapped[Cycle] = mapped_column(
        pg_enum(Cycle, "cycle"),
        nullable=False,
        comment="Type de lycée concerné (moderne ou technique)",
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # --- Relations ---
    level_associations: Mapped[list["LevelSeries"]] = relationship(
        "LevelSeries",
        back_populates="series",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Series code={self.code} cycle={self.cycle.value}>"


class LevelSeries(Base):
    """Association many-to-many ``Level`` ↔ ``Series``.

    Permet de modéliser qu'une série (ex: ``A4``) est disponible sur plusieurs
    niveaux (``1ère`` et ``Terminale``), et qu'un niveau (ex: ``Terminale``
    moderne) propose plusieurs séries (``A4``, ``C``, ``D``).
    """

    __tablename__ = "level_series"
    __table_args__ = (
        UniqueConstraint("level_id", "series_id", name="uq_level_series"),
        Index("ix_level_series_series_id", "series_id"),
        {"comment": "Séries disponibles par niveau (many-to-many)"},
    )

    level_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("levels.id", ondelete="CASCADE"),
        primary_key=True,
    )
    series_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("series.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # --- Relations ---
    level: Mapped[Level] = relationship("Level", back_populates="series_associations")
    series: Mapped[Series] = relationship("Series", back_populates="level_associations")

    def __repr__(self) -> str:
        return f"<LevelSeries level={self.level_id} series={self.series_id}>"


class Subject(UUIDMixin, TimestampMixin, Base):
    """Matière scolaire.

    Exemples : "Mathématiques", "SVT", "Philosophie", "Mécanique".
    """

    __tablename__ = "subjects"
    __table_args__ = (
        UniqueConstraint("name", name="uq_subjects_name"),
        {"comment": "Matières scolaires"},
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cycle: Mapped[Cycle | None] = mapped_column(
        pg_enum(Cycle, "cycle"),
        nullable=True,
        comment="Cycle concerné (NULL = matière transverse à tous les cycles)",
    )

    chapters: Mapped[list["Chapter"]] = relationship(
        "Chapter",
        back_populates="subject",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    def __repr__(self) -> str:
        return f"<Subject name={self.name}>"


class Chapter(UUIDMixin, TimestampMixin, Base):
    """Chapitre d'une matière pour un niveau et une série donnés.

    Le couple ``(level_id, subject_id)`` détermine la classe et la matière.
    ``series_id`` est optionnel : il n'est renseigné que pour les chapitres
    spécifiques à une série (ex: "Mécanique" uniquement en Terminale F1).

    Pour les chapitres communs à toutes les séries d'un niveau (ex: "Algèbre"
    en 3ème), ``series_id`` reste ``NULL``.
    """

    __tablename__ = "chapters"
    __table_args__ = (
        UniqueConstraint(
            "level_id", "subject_id", "series_id", "order_index",
            name="uq_chapters_level_subject_series_order",
        ),
        Index("ix_chapters_level_id", "level_id"),
        Index("ix_chapters_subject_id", "subject_id"),
        Index("ix_chapters_series_id", "series_id"),
        {"comment": "Chapitres du programme officiel togolais"},
    )

    level_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("levels.id", ondelete="CASCADE"),
        nullable=False,
    )
    subject_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
    )
    series_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("series.id", ondelete="SET NULL"),
        nullable=True,
        comment="Série spécifique (NULL si chapitre commun à toutes les séries)",
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Ordre dans l'année scolaire (1, 2, 3...)",
    )

    level: Mapped[Level] = relationship("Level", back_populates="chapters")
    subject: Mapped[Subject] = relationship("Subject", back_populates="chapters")
    series: Mapped[Series | None] = relationship("Series", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Chapter title={self.title} order={self.order_index}>"