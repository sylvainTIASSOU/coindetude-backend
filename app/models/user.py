"""Modèles utilisateurs et profils spécialisés.

Contient :
- ``User`` : table principale (tous rôles confondus).
- ``StudentProfile`` : données spécifiques aux élèves (niveau, XP, streak).
- ``ParentProfile`` : données spécifiques aux parents.
- ``TeacherProfile`` : données spécifiques aux enseignants.
- ``ParentStudent`` : table de liaison parent ↔ élève.

⚠️ Les modèles pédagogiques (``Level``, ``Subject``, ``Chapter``) ont été
déplacés vers ``app/models/educational.py`` pour préparer L3.
"""

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
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,  # noqa: F401
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import (
    TeacherVerificationStatus,
    UserRole,
    pg_enum,
)

if TYPE_CHECKING:
    # Imports uniquement pour les type hints (évite les cycles)
    from app.models.auth import RefreshToken
    from app.models.educational import Level, Series
    from app.models.file import StoredFile  # noqa: F401
    from app.models.notification import (
        DeviceToken,  # noqa: F401
        NotificationPreference,  # noqa: F401
        SentNotification,  # noqa: F401
    )
    from app.models.payment import Subscription, Transaction  # noqa: F401


class User(UUIDMixin, TimestampMixin, Base):
    """Utilisateur de la plateforme, tous rôles confondus.

    Le rôle (``role``) détermine quel profil spécialisé est associé :
    ``StudentProfile``, ``ParentProfile`` ou ``TeacherProfile``.
    """

    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_role", "role"),
        Index("ix_users_is_active", "is_active"),
        {"comment": "Comptes utilisateurs (élèves, parents, enseignants, admins)"},
    )

    # --- Identité ---
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # --- Identifiants de connexion ---
    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
        comment="Numéro de téléphone au format international (+228...)",
    )
    email: Mapped[str | None] = mapped_column(
        String(150),
        unique=True,
        nullable=True,
        index=True,
        comment="Email optionnel (les élèves n'en ont pas toujours)",
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Hash Argon2id du mot de passe",
    )

    # --- Rôle & profil ---
    role: Mapped[UserRole] = mapped_column(
        pg_enum(UserRole, "user_role"),
        nullable=False,
        default=UserRole.STUDENT,
        index=True,
    )
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    # --- Avatar (FK différée pour casser le cycle users ↔ stored_files) ---
    avatar_file_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "stored_files.id",
            use_alter=True,  # FK ajoutée après création des deux tables
            name="fk_users_avatar_file_id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    # --- État du compte ---
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    phone_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="NULL = numéro non vérifié. Renseigné après /verify-otp.",
    )
    @property
    def is_phone_verified(self) -> bool:
        return self.phone_verified_at is not None # type: ignore

    # --- Relations ---
    student_profile: Mapped[StudentProfile | None] = relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    parent_profile: Mapped[ParentProfile | None] = relationship(
        "ParentProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    teacher_profile: Mapped[TeacherProfile | None] = relationship(
        "TeacherProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    refresh_tokens: Mapped[list[RefreshToken]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} phone={self.phone} role={self.role.value}>"


class StudentProfile(Base):
    """Profil spécialisé pour les élèves.

    Relation 1-1 avec ``User``. Contient les données de progression
    pédagogique : niveau, série, XP, streaks, code de liaison parent.

    ⚠️ La cohérence ``level.cycle == series.cycle`` est validée côté API
    (Pydantic validator), pas en SQL.
    """

    __tablename__ = "student_profiles"
    __table_args__ = (
        Index("ix_student_profiles_level_id", "level_id"),
        Index("ix_student_profiles_series_id", "series_id"),
        {"comment": "Données spécifiques aux élèves (niveau, série, gamification)"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    level_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("levels.id", ondelete="SET NULL"),
        nullable=True,
        comment="Classe actuelle (ex: Terminale). Nullable si non renseigné.",
    )
    series_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("series.id", ondelete="SET NULL"),
        nullable=True,
        comment="Série du lycée (A4, C, D, F1...). NULL pour les collégiens.",
    )

    # --- Gamification (inchangé) ---
    xp_points: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0",
    )
    current_streak: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0",
    )
    longest_streak: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0",
    )

    last_streak_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Dernière date à laquelle un streak a été compté (UTC)",
    )

    # --- Liaison parent (inchangé) ---
    pairing_code: Mapped[str] = mapped_column(
        String(6), unique=True, nullable=False, index=True,
        comment="Code à 6 caractères permettant à un parent de s'abonner",
    )

    # --- Relations ---
    user: Mapped[User] = relationship("User", back_populates="student_profile")
    level: Mapped["Level | None"] = relationship("Level", lazy="selectin")
    series: Mapped["Series | None"] = relationship("Series", lazy="selectin")

    def __repr__(self) -> str:
        return f"<StudentProfile user_id={self.user_id} xp={self.xp_points}>"
class ParentProfile(Base):
    """Profil spécialisé pour les parents."""

    __tablename__ = "parent_profiles"
    __table_args__ = (
        {"comment": "Données spécifiques aux parents d'élèves"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    job_title: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Profession (statistiques agrégées uniquement)",
    )

    user: Mapped[User] = relationship("User", back_populates="parent_profile")

    def __repr__(self) -> str:
        return f"<ParentProfile user_id={self.user_id}>"


class TeacherProfile(Base):
    """Profil spécialisé pour les enseignants (Marketplace V2)."""

    __tablename__ = "teacher_profiles"
    __table_args__ = (
        {"comment": "Données spécifiques aux enseignants (Marketplace V2)"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    school_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    verification_status: Mapped[TeacherVerificationStatus] = mapped_column(
        pg_enum(TeacherVerificationStatus, "teacher_verification_status"),
        nullable=False,
        default=TeacherVerificationStatus.PENDING,
        server_default=TeacherVerificationStatus.PENDING.value,
    )

    user: Mapped[User] = relationship("User", back_populates="teacher_profile")

    def __repr__(self) -> str:
        return f"<TeacherProfile user_id={self.user_id}>"


class ParentStudent(Base):
    """Table de liaison many-to-many parent ↔ élève.

    Permet à un parent de suivre plusieurs enfants, et à un élève d'avoir
    plusieurs parents/tuteurs enregistrés.
    """

    __tablename__ = "parent_student"
    __table_args__ = (
        UniqueConstraint("parent_id", "student_id", name="uq_parent_student"),
        Index("ix_parent_student_student_id", "student_id"),
        {"comment": "Liaison parent ↔ élève (many-to-many)"},
    )

    parent_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    student_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f"<ParentStudent parent={self.parent_id} student={self.student_id}>"
