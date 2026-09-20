"""Modèles des abonnements Mobile Money et de l'historique des transactions.

⚠️ Depuis L4, ``Subscription`` référence un ``Plan`` (FK) plutôt que
d'utiliser directement l'enum ``PlanType``. Cela permet de modifier les
prix/durées/avantages sans migration ni redéploiement.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import (
    PaymentProvider,
    TransactionStatus,
    pg_enum,
)

if TYPE_CHECKING:
    from app.models.plan import Plan
    from app.models.user import User


class Subscription(UUIDMixin, TimestampMixin, Base):
    """Abonnement d'un utilisateur à un forfait.

    Le forfait souscrit est identifié par ``plan_id``. Le snapshot
    ``plan_code`` (dénormalisé) permet d'auditer facilement l'historique
    même si le plan change de code ultérieurement.

    Le forfait ``freemium`` n'a pas de date de fin. Les autres forfaits ont
    une ``end_date`` calculée à partir de ``plan.duration_days`` au moment
    de la souscription.
    """

    __tablename__ = "subscriptions"
    __table_args__ = (
        Index("ix_subscriptions_user_id_is_active", "user_id", "is_active"),
        Index("ix_subscriptions_plan_id", "plan_id"),
        Index("ix_subscriptions_end_date", "end_date"),
        {"comment": "Abonnements Mobile Money des utilisateurs"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    plan_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("plans.id", ondelete="RESTRICT"),
        nullable=False,
        comment="RESTRICT : un plan utilisé ne peut pas être supprimé",
    )
    plan_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Snapshot dénormalisé du code du plan (audit)",
    )
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="NULL pour le forfait freemium",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true",
    )

    user: Mapped["User"] = relationship("User", lazy="noload")
    plan: Mapped["Plan"] = relationship("Plan", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Subscription id={self.id} plan={self.plan_code} active={self.is_active}>"


class Transaction(UUIDMixin, Base):
    """Transaction Mobile Money (log immuable).

    ⚠️ ``external_ref`` est unique pour garantir l'idempotence des webhooks.
    """

    __tablename__ = "transactions"
    __table_args__ = (
        UniqueConstraint("external_ref", name="uq_transactions_external_ref"),
        Index("ix_transactions_user_id_created_at", "user_id", "created_at"),
        Index("ix_transactions_status", "status"),
        {"comment": "Historique des paiements Mobile Money"},
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False,
        comment="Montant en FCFA",
    )
    provider: Mapped[PaymentProvider] = mapped_column(
        pg_enum(PaymentProvider, "payment_provider"),
        nullable=False,
    )
    status: Mapped[TransactionStatus] = mapped_column(
        pg_enum(TransactionStatus, "transaction_status"),
        nullable=False,
        default=TransactionStatus.PENDING,
        server_default=TransactionStatus.PENDING.value,
    )
    external_ref: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False,
        comment="Référence de l'agrégateur (PayGate/CinetPay/FedaPay)",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship("User", lazy="noload")

    def __repr__(self) -> str:
        return f"<Transaction id={self.id} status={self.status.value} amount={self.amount}>"