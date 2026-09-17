import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models._base import created_at_col, updated_at_col


class Level(Base):
    __tablename__ = "levels"
    __table_args__ = (CheckConstraint("cycle IN ('college','lycee')", name="ck_niveaux_cycle"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cycle: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = created_at_col()
    updated_at: Mapped[datetime] = updated_at_col()

    chapters: Mapped[list["Chapter"]] = relationship(back_populates="level")


class Matter(Base):
    __tablename__ = "matters"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    chapters: Mapped[list["Chapter"]] = relationship(back_populates="matter")


class LevelMatter(Base):
    __tablename__ = "level_matters"
    __table_args__ = (UniqueConstraint("level_id", "matter_id", name="uq_level_matter"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    level_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("levels.id"), nullable=False)
    matter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("matters.id"), nullable=False)

    level: Mapped["Level"] = relationship(back_populates="level_matters")
    matter: Mapped["Matter"] = relationship(back_populates="level_matters")


class Chapter(Base):
    __tablename__ = "chapters"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    title: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    level_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("levels.id"), nullable=False)
    matter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("matters.id"), nullable=False)

    created_at: Mapped[datetime] = created_at_col()
    updated_at: Mapped[datetime] = updated_at_col()
    level: Mapped["Level"] = relationship(back_populates="chapters")
    matter: Mapped["Matter"] = relationship(back_populates="chapters")

    # ressources: Mapped[list["Ressource"]] = relationship(back_populates="chapitre")
