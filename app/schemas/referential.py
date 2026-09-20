"""Schémas Pydantic du référentiel pédagogique.

Convention :
- ``*Read`` : sortie API (lecture publique)
- ``*ReadDetail`` : sortie détaillée (avec champs lourds)
- ``*Create`` : entrée admin (création)
- ``*Update`` : entrée admin (mise à jour partielle)
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models import (
    Cycle,
    ResourceOrigin,
    ResourceType,
)


# =============================================================================
# LEVEL
# =============================================================================

class LevelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    cycle: Cycle
    order_index: int


class LevelCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "2nde",
                "cycle": "lycee_moderne",
                "order_index": 5,
            }
        },
    )

    name: str = Field(..., min_length=1, max_length=50)
    cycle: Cycle
    order_index: int = Field(0, ge=0)


class LevelUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(None, min_length=1, max_length=50)
    cycle: Cycle | None = None
    order_index: int | None = Field(None, ge=0)


# =============================================================================
# SERIES
# =============================================================================

class SeriesRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    cycle: Cycle
    description: str | None


class SeriesCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "code": "A4",
                "name": "Série A4 - Littéraire et Langues",
                "cycle": "lycee_moderne",
                "description": "Série orientée lettres et langues vivantes.",
            }
        },
    )

    code: str = Field(..., min_length=1, max_length=10)
    name: str = Field(..., min_length=1, max_length=150)
    cycle: Cycle
    description: str | None = None


class SeriesUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str | None = Field(None, min_length=1, max_length=10)
    name: str | None = Field(None, min_length=1, max_length=150)
    cycle: Cycle | None = None
    description: str | None = None


# =============================================================================
# SUBJECT
# =============================================================================

class SubjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    icon_url: str | None
    cycle: Cycle | None


class SubjectCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "Mathématiques",
                "icon_url": "https://cdn.coindetude.tg/icons/maths.svg",
                "cycle": None,
            }
        },
    )

    name: str = Field(..., min_length=1, max_length=100)
    icon_url: str | None = Field(None, max_length=255)
    cycle: Cycle | None = Field(
        None, description="NULL = matière transverse à tous les cycles"
    )


class SubjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(None, min_length=1, max_length=100)
    icon_url: str | None = Field(None, max_length=255)
    cycle: Cycle | None = None


# =============================================================================
# CHAPTER
# =============================================================================

class ChapterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    level_id: UUID
    subject_id: UUID
    series_id: UUID | None
    title: str
    description: str | None
    order_index: int


class ChapterCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "level_id": "550e8400-e29b-41d4-a716-446655440000",
                "subject_id": "550e8400-e29b-41d4-a716-446655440001",
                "series_id": None,
                "title": "Théorème de Thalès",
                "description": "Configurations et applications",
                "order_index": 3,
            }
        },
    )

    level_id: UUID
    subject_id: UUID
    series_id: UUID | None = Field(
        None, description="NULL si chapitre commun à toutes les séries"
    )
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    order_index: int = Field(..., ge=0)


class ChapterUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    level_id: UUID | None = None
    subject_id: UUID | None = None
    series_id: UUID | None = None
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    order_index: int | None = Field(None, ge=0)


# =============================================================================
# RESOURCE
# =============================================================================

class ResourceRead(BaseModel):
    """Vue allégée (pas de ``content_text``) pour les listes."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    chapter_id: UUID | None
    type: ResourceType
    title: str
    file_id: UUID | None
    year: int | None
    origin: ResourceOrigin


class ResourceReadDetail(ResourceRead):
    """Vue détaillée avec ``content_text`` + URL S3 presign si file."""

    content_text: str | None = None
    file_url: str | None = Field(
        None, description="URL presignée (TTL 1h) si le fichier existe"
    )


class ResourceCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "chapter_id": "550e8400-e29b-41d4-a716-446655440000",
                "type": "cours",
                "title": "Théorème de Thalès — cours",
                "content_text": "# Théorème de Thalès\n\n...",
                "file_id": None,
                "year": None,
                "origin": "admin",
            }
        },
    )

    chapter_id: UUID | None = None
    type: ResourceType
    title: str = Field(..., min_length=1, max_length=255)
    content_text: str | None = Field(
        None, description="Contenu Markdown affichable directement"
    )
    file_id: UUID | None = Field(
        None, description="FK vers stored_files (PDF)"
    )
    year: int | None = Field(None, ge=1980, le=2100)
    origin: ResourceOrigin = ResourceOrigin.ADMIN


class ResourceUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chapter_id: UUID | None = None
    type: ResourceType | None = None
    title: str | None = Field(None, min_length=1, max_length=255)
    content_text: str | None = None
    file_id: UUID | None = None
    year: int | None = Field(None, ge=1980, le=2100)
    origin: ResourceOrigin | None = None
