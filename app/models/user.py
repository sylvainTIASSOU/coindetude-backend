"""Modèle exemple — à remplacer/étendre par le schéma des 26 tables déjà validé.

Sert de gabarit pour la syntaxe SQLAlchemy 2.0 (Mapped / mapped_column)
à réutiliser sur les autres tables (référentiel pédagogique, contenu,
paiement, etc.).
"""

import uuid
from enum import StrEnum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


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
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), default=UserRole.ELEVE
    )
    is_active: Mapped[bool] = mapped_column(default=True)
