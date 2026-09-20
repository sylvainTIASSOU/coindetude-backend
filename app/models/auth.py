"""Modèles d'authentification et d'idempotence.

Contient :
- ``RefreshToken`` : gestion des refresh tokens avec rotation à usage unique
  et détection de réutilisation (vol de token).
- ``IdempotencyKey`` : stockage des réponses pour garantir l'idempotence stricte
  sur les endpoints critiques (``/sync/apply-event``, ``/telemetry/ingest``).
"""

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
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(UUIDMixin, Base):
    """Refresh token JWT avec rotation à usage unique.

    **Modèle de sécurité** :

    1. À chaque login, un nouveau ``family_id`` (UUID) est généré.
    2. Le token est stocké sous forme de **hash SHA-256** (jamais en clair).
    3. Lors d'un refresh, l'ancien token est marqué ``revoked_at=now()`` et
       ``replaced_by_id`` pointe vers le nouveau token de la même famille.
    4. Si un token déjà révoqué est présenté → **réutilisation détectée** →
       toute la famille est révoquée immédiatement (protection contre le vol).

    Le hash SHA-256 (et non Argon2) est utilisé pour permettre une vérification
    rapide à chaque requête. Le token JWT lui-même a une entropie suffisante
    (signature HMAC + payload signé) pour résister aux attaques par force brute.
    """

    __tablename__ = "refresh_tokens"
    __table_args__ = (
        Index("ix_refresh_tokens_family_id", "family_id"),
        Index("ix_refresh_tokens_user_id", "user_id"),
        Index("ix_refresh_tokens_expires_at", "expires_at"),
        {"comment": "Refresh tokens JWT avec rotation et détection de réutilisation"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    family_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        comment="Identifiant de la chaîne de tokens (un login = une famille)",
    )
    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
        comment="SHA-256 hexadécimal du refresh token (jamais en clair)",
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Date de révocation. NULL = token actif.",
    )
    replaced_by_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("refresh_tokens.id", ondelete="SET NULL"),
        nullable=True,
        comment="Nouveau token issu de la rotation (chaînage)",
    )

    # --- Traçabilité sécurité ---
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # --- Relations ---
    user: Mapped[User] = relationship("User", back_populates="refresh_tokens")

    @property
    def is_active(self) -> bool:
        """Un token est actif s'il n'est ni révoqué ni expiré."""
        return self.revoked_at is None

    def __repr__(self) -> str:
        status = "revoked" if self.revoked_at else "active"
        return f"<RefreshToken family={self.family_id} status={status}>"


class IdempotencyKey(UUIDMixin, TimestampMixin, Base):
    """Stockage des réponses d'endpoints idempotents.

    Utilisé par :

    - ``POST /api/v1/sync/apply-event`` (header ``Idempotency-Key`` obligatoire)
    - ``POST /api/v1/telemetry/ingest`` (champ ``client_batch_id``)

    **Principe** : à la première réception d'une clé, le serveur exécute
    l'opération et stocke la réponse complète (status + body). Toute réception
    ultérieure de la même clé retourne la réponse stockée **sans réexécuter**
    l'opération.

    **Portée** : la clé est unique par ``(user_id, scope, key)``. Le ``scope``
    permet d'utiliser le même UUID sur deux endpoints différents sans collision.

    **Nettoyage** : les clés plus vieilles que ``expires_at`` sont supprimées
    périodiquement par un job ARQ (à venir en L3+).
    """

    __tablename__ = "idempotency_keys"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "scope", "key", name="uq_idempotency_user_scope_key"
        ),
        Index("ix_idempotency_expires_at", "expires_at"),
        {"comment": "Clés d'idempotence pour sync et télémétrie"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    scope: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Endpoint concerné (ex: 'sync:apply-event')",
    )
    key: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="UUID v4 fourni par le client (header ou body)",
    )
    request_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="SHA-256 du body de la requête (détecte les abus de clé)",
    )
    response_status: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Code HTTP de la réponse originale (200, 201, 409...)",
    )
    response_body: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        comment="Body JSON de la réponse originale (rejoué tel quel)",
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Date d'expiration de la clé (TTL recommandé : 7 jours)",
    )

    def __repr__(self) -> str:
        return f"<IdempotencyKey scope={self.scope} key={self.key[:8]}...>"
