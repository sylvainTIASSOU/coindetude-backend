"""Modèle exemple — à remplacer/étendre par le schéma des 26 tables déjà validé.

Sert de gabarit pour la syntaxe SQLAlchemy 2.0 (Mapped / mapped_column)
à réutiliser sur les autres tables (référentiel pédagogique, contenu,
paiement, etc.).
"""

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models._base import created_at_col, updated_at_col


class UserRole(StrEnum):
    ELEVE = "eleve"
    PARENT = "parent"
    ENSEIGNANT = "enseignant"
    ADMIN = "admin"


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), default=UserRole.ELEVE)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    profile_url: Mapped[str] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = created_at_col()
    updated_at: Mapped[datetime] = updated_at_col()

    level_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("levels.id"))

    # progression: Mapped[list["ProgressionEleve"]] = relationship(back_populates="utilisateur")
    # abonnements: Mapped[list["Abonnement"]] = relationship(back_populates="utilisateur")
    # device_tokens: Mapped[list["DeviceToken"]] = relationship(back_populates="utilisateur")
    # profil_examen: Mapped[Optional["ProfilExamen"]] = relationship(back_populates="utilisateur")
