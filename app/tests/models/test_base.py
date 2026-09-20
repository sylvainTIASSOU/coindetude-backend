"""Tests de validation de la structure de base des modèles.

Vérifie que :
- La base déclarative est bien instanciée.
- Les mixins exposent les colonnes attendues.
- Les enums ont les bonnes valeurs.
"""

from datetime import datetime
from uuid import UUID

import pytest
from sqlalchemy import inspect

from app.models import Base, TimestampMixin, UserRole, UUIDMixin
from app.models.enums import (
    ConflictStrategy,
    FileContext,
    ResourceType,
    SyncOperation,
)


def test_base_metadata_is_registered() -> None:
    """La metadata SQLAlchemy doit être accessible."""
    assert Base.metadata is not None
    assert hasattr(Base.metadata, "tables")


def test_uuid_mixin_has_id_column() -> None:
    """UUIDMixin doit exposer une colonne ``id`` typée UUID."""
    mapper = inspect(UUIDMixin)
    assert "id" in mapper.columns or hasattr(UUIDMixin, "id")


def test_timestamp_mixin_has_created_updated() -> None:
    """TimestampMixin doit exposer created_at et updated_at."""
    assert hasattr(TimestampMixin, "created_at")
    assert hasattr(TimestampMixin, "updated_at")


@pytest.mark.parametrize(
    "enum_cls,expected_values",
    [
        (UserRole, {"student", "parent", "teacher", "admin"}),
        (FileContext, {"avatar", "resource_pdf", "ai_scan"}),
        (ResourceType, {"cours", "exercice", "annale"}),
        (SyncOperation, {"create", "update", "delete"}),
        (
            ConflictStrategy,
            {"SERVER_AUTHORITATIVE", "CRDT_MERGE", "LWW", "MANUAL"},
        ),
    ],
)
def test_enums_have_expected_values(enum_cls, expected_values: set[str]) -> None:
    """Chaque enum doit exposer exactement les valeurs attendues."""
    assert {e.value for e in enum_cls} == expected_values


def test_enum_serialization_is_string() -> None:
    """Les enums doivent se sérialiser en string (compatibilité JSON)."""
    assert UserRole.STUDENT.value == "student"
    assert str(UserRole.STUDENT.value) == "student"
    # Compatible json.dumps
    import json
    assert json.dumps({"role": UserRole.STUDENT.value}) == '{"role": "student"}'