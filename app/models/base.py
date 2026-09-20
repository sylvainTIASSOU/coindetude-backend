"""Base déclarative SQLAlchemy 2.0 pour tous les modèles CoinDetude.

Fournit :
- ``Base`` : classe déclarative commune (héritage ``DeclarativeBase``).
- ``UUIDMixin`` : ajoute une clé primaire UUID v4.
- ``TimestampMixin`` : ajoute ``created_at`` / ``updated_at`` gérés côté serveur.

Toutes les tables utilisent UUID + timestamptz pour rester cohérentes avec
le contrat d'API offline-first (les clients peuvent générer leurs propres UUID
avant synchronisation).
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class UUIDMixin:
    """Ajoute une clé primaire UUID v4.

    Utilisé pour toutes les tables CoinDetude. Les clients Flutter génèrent
    également des UUID avant synchronisation (Outbox Pattern), ce qui garantit
    l'idempotence des créations côté serveur.
    """

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )


class TimestampMixin:
    """Ajoute ``created_at`` et ``updated_at``.

    Les deux colonnes sont gérées **côté serveur** (``server_default`` /
    ``onupdate``) pour éviter toute dépendance à l'horloge client — crucial
    en contexte offline-first où les horloges peuvent dériver.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
