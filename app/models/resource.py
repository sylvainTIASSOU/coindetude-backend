"""Modèle des ressources pédagogiques (cours, exercices, annales).

Une ressource est rattachée à un chapitre (sauf pour les annales générales
qui couvrent tout un examen) et peut être soit du texte Markdown directement
affichable, soit un PDF stocké sur S3/MinIO/R2.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import ResourceOrigin, ResourceType, pg_enum

if TYPE_CHECKING:
    pass


class Resource(UUIDMixin, TimestampMixin, Base):
    """Ressource pédagogique officielle ou communautaire.

    Trois types possibles :
    - ``cours`` : cours de référence aligné sur le programme officiel.
    - ``exercice`` : exercices d'entraînement avec corrigé.
    - ``annale`` : sujet d'examen national (BEPC, BAC 1, BAC 2) + corrigé.
    """

    __tablename__ = "resources"
    __table_args__ = (
        Index("ix_resources_chapter_id", "chapter_id"),
        Index("ix_resources_type_year", "type", "year"),
        Index("ix_resources_origin", "origin"),
        {"comment": "Ressources pédagogiques (cours, exercices, annales)"},
    )

    chapter_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("chapters.id", ondelete="SET NULL"),
        nullable=True,
        comment="NULL pour les annales générales (ex: sujet BAC toutes matières)",
    )
    type: Mapped[ResourceType] = mapped_column(
        pg_enum(ResourceType, "resource_type"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Contenu Markdown directement lisible dans l'app (léger)",
    )
    file_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("stored_files.id", ondelete="SET NULL"),
        nullable=True,
        comment="PDF rattaché (lourd, chargé à la demande)",
    )
    year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Année d'édition (utile uniquement pour les annales)",
    )
    origin: Mapped[ResourceOrigin] = mapped_column(
        pg_enum(ResourceOrigin, "resource_origin"),
        nullable=False,
        default=ResourceOrigin.ADMIN,
        server_default=ResourceOrigin.ADMIN.value,
    )

    chapter: Mapped["object | None"] = relationship(  # type: ignore[assignment]
        "Chapter",
        lazy="noload",
    )

    def __repr__(self) -> str:
        return f"<Resource id={self.id} type={self.type.value} title={self.title}>"