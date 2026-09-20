"""Politiques de validation des uploads (taille, MIME, extension, key)."""

from __future__ import annotations


from pathlib import Path
from uuid import UUID

from app.core.config import settings
from app.models.enums import FileContext, UploadPurpose
from app.services.storage.uploads.errors import UploadPolicyError

from app.core.logging import log as logger


# Mapping purpose (API) → context (DB) → taille max (KB)
_PURPOSE_MAP: dict[UploadPurpose, tuple[FileContext, int]] = {
    UploadPurpose.AVATAR: (
        FileContext.AVATAR,
        settings.UPLOAD_MAX_SIZE_KB_AVATAR,
    ),
    UploadPurpose.HOMEWORK_SCAN: (
        FileContext.AI_SCAN,
        settings.UPLOAD_MAX_SIZE_KB_DOCUMENT,
    ),
    UploadPurpose.RESOURCE_PDF: (
        FileContext.RESOURCE_PDF,
        settings.UPLOAD_MAX_SIZE_KB_DOCUMENT,
    ),
}


# Extension attendue par MIME (whitelist stricte)
_MIME_TO_EXT: dict[str, str] = {
    "image/webp": "webp",
    "image/jpeg": "jpg",
    "image/png": "png",
    "application/pdf": "pdf",
}


def resolve_policy(
    purpose: UploadPurpose, mime_type: str, size_kb: int
) -> tuple[FileContext, str]:
    """Valide la politique et retourne ``(context, extension)``.

    Raises:
        UploadPolicyError: si le MIME n'est pas whitelisté ou si la taille
            dépasse la limite du purpose.
    """
    context, max_kb = _PURPOSE_MAP[purpose]

    if mime_type not in settings.UPLOAD_ALLOWED_MIME_TYPES:
        raise UploadPolicyError(
            f"Type MIME non autorisé : {mime_type}. "
            f"Autorisés : {', '.join(settings.UPLOAD_ALLOWED_MIME_TYPES)}."
        )

    if size_kb <= 0:
        raise UploadPolicyError("La taille doit être strictement positive.")

    if size_kb > max_kb:
        raise UploadPolicyError(
            f"Fichier trop volumineux : {size_kb} KB > {max_kb} KB "
            f"pour le purpose '{purpose.value}'."
        )

    ext = _MIME_TO_EXT.get(mime_type)
    if ext is None:
        raise UploadPolicyError(f"Aucune extension mappée pour {mime_type}.")

    return context, ext


def build_s3_key(
    *,
    context: FileContext,
    user_id: UUID,
    file_id: UUID,
    extension: str,
) -> str:
    """Construit une clé S3 structurée et non-devinable.

    Format : ``{context}/{user_id}/{file_id}.{ext}``
    """
    return f"{context.value}/{user_id}/{file_id}.{extension}"


def safe_filename(original: str | None, extension: str) -> str:
    """Retourne un nom de fichier sûr et borné.

    Empêche les path traversals et les noms absurdes.
    """
    if not original:
        return f"upload.{extension}"
    name = Path(original).name[:200]  # strip path, cap length
    if not name.lower().endswith(f".{extension}"):
        name = f"{Path(name).stem[:190]}.{extension}"
    return name
