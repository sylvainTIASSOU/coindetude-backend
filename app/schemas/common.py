"""Schémas génériques réutilisables (pagination, etc.)."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageParams(BaseModel):
    """Paramètres de pagination offset-based."""

    limit: int = Field(50, ge=1, le=200)
    offset: int = Field(0, ge=0)


class PageResponse(BaseModel, Generic[T]):
    """Réponse paginée générique."""

    items: list[T]
    total: int = Field(..., description="Nombre total d'éléments (toutes pages)")
    limit: int
    offset: int
    has_more: bool = Field(..., description="True s'il reste des éléments après cette page")
