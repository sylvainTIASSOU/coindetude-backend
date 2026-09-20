"""Modèle du catalogue des forfaits Mobile Money.

La table ``plans`` contient **tous les paramètres affichables** dans l'app
avant qu'un élève ne s'abonne : nom, description, prix, durée, avantages,
ordre d'affichage. Les abonnements (``subscriptions``) pointent vers un plan.

Permet à TKMS de :
- modifier un prix sans redéployer l'app Flutter ;
- ajouter un nouveau forfait (ex: ``pass_trimestre``) sans migration ;
- activer/désactiver un forfait (``is_active``) sans le supprimer.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Boolean,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.enums import PlanType, pg_enum


class Plan(UUIDMixin, TimestampMixin, Base):
    """Forfait Mobile Money (freemium ou payant).

    Le ``code`` (``PlanType``) identifie le forfait dans le code applicatif
    (règles métier : "un pass_jour donne accès à X scans"). Le ``name`` et la
    ``description`` sont affichés tels quels à l'élève.
    """

    __tablename__ = "plans"
    __table_args__ = (
        UniqueConstraint("code", name="uq_plans_code"),
        Index("ix_plans_is_active_order_index", "is_active", "order_index"),
        {"comment": "Catalogue des forfaits Mobile Money"},
    )

    code: Mapped[PlanType] = mapped_column(
        pg_enum(PlanType, "plan_type"),
        nullable=False,
        unique=True,
        comment="Identifiant technique du forfait (freemium, pass_jour...)",
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nom affiché (ex: 'Pass Jour')",
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Description courte affichée sur la carte du forfait",
    )
    price_fcfa: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
        comment="Prix en FCFA (0 pour le freemium)",
    )
    duration_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Durée en jours (0 = illimité pour freemium)",
    )
    advantages: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default="[]",
        comment="Liste des avantages à afficher (JSONB)",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="Si FALSE, le forfait n'est plus proposé à l'achat",
    )
    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Ordre d'affichage dans l'app (croissant)",
    )

    def __repr__(self) -> str:
        return f"<Plan code={self.code.value} price={self.price_fcfa}>"