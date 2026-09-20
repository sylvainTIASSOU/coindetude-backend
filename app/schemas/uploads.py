"""Schémas Pydantic pour /uploads."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models import FileStatus, UploadPurpose


class PresignRequest(BaseModel):
    """Corps de POST /uploads/presign."""

    model_config = ConfigDict(extra="forbid")

    file_name: str | None = Field(None, max_length=255)
    file_type: str = Field(
        ...,
        description="MIME type (whitelist : image/webp, image/jpeg, application/pdf)",
    )
    size_kb: int = Field(..., gt=0, le=10_000)
    purpose: UploadPurpose


class PresignResponse(BaseModel):
    file_id: UUID
    s3_key: str
    upload_url: str
    method: str = "PUT"
    headers: dict[str, str]
    expires_at: datetime


class ConfirmResponse(BaseModel):
    file_id: UUID
    status: FileStatus
    size_kb: int
    mime_type: str
    url: str
    uploaded_at: datetime
