"""Orchestrateur du module uploads.

**Flow complet** :

1. ``presign`` :
   - Valide la politique (purpose + MIME + taille déclarée).
   - Crée la row ``stored_files`` avec ``status=pending``.
   - Génère une URL PUT pré-signée pour la clé S3 associée.
   - Retourne ``{upload_url, file_id, s3_key, expires_at}``.

2. ``confirm`` :
   - Récupère la row ``stored_files`` (doit appartenir au user).
   - Vérifie qu'elle est bien ``pending``.
   - ``head_object`` sur S3 → existence + taille réelle.
   - Si OK : passe ``status=uploaded``, ``size_kb_actual``, ``uploaded_at``.
   - Si taille réelle > max : supprime l'objet S3, marque ``failed``.
   - Retourne ``{file_id, status, url}`` (URL GET presign 1h).
"""

from __future__ import annotations


from datetime import timedelta
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import utcnow
from app.models import FileStatus, StoredFile, UploadPurpose
from app.services.storage.s3_client import S3Client, get_s3_client
from app.services.storage.uploads.errors import (
    FileAlreadyConfirmed,
    FileNotFoundError_,
    FileNotUploadedToStorage,
    FileSizeMismatch,
)
from app.services.storage.uploads.policies import (
    build_s3_key,
    resolve_policy,
    safe_filename,
)

from app.core.logging import log as logger


class UploadsService:
    def __init__(
        self, session: AsyncSession, s3: S3Client | None = None
    ) -> None:
        self.session = session
        self.s3 = s3 or get_s3_client()

    # ------------------------------------------------------------------
    # Presign
    # ------------------------------------------------------------------

    async def presign(
        self,
        *,
        user_id: UUID,
        file_name: str | None,
        file_type: str,
        size_kb: int,
        purpose: UploadPurpose,
    ) -> dict:
        context, ext = resolve_policy(purpose, file_type, size_kb)
        file_id = uuid4()
        key = build_s3_key(
            context=context,
            user_id=user_id,
            file_id=file_id,
            extension=ext,
        )

        upload_url = await self.s3.presign_put(
            key=key,
            content_type=file_type,
            expires_in=settings.UPLOAD_PRESIGN_TTL_SECONDS,
        )

        record = StoredFile(
            id=file_id,
            uploader_id=user_id,
            file_name=safe_filename(file_name, ext),
            file_path=key,
            mime_type=file_type,
            context=context,
            status=FileStatus.PENDING,
            size_kb_declared=size_kb,
            expires_at=utcnow()
            + timedelta(hours=settings.UPLOAD_PENDING_TTL_HOURS),
        )
        self.session.add(record)
        await self.session.flush()

        return {
            "file_id": file_id,
            "s3_key": key,
            "upload_url": upload_url,
            "method": "PUT",
            "headers": {"Content-Type": file_type},
            "expires_at": upload_url and record.expires_at,
        }

    # ------------------------------------------------------------------
    # Confirm
    # ------------------------------------------------------------------

    async def confirm(
        self, *, user_id: UUID, file_id: UUID
    ) -> dict:
        record = await self.session.get(StoredFile, file_id)
        if record is None or record.uploader_id != user_id:
            raise FileNotFoundError_()

        if record.status is FileStatus.UPLOADED:
            raise FileAlreadyConfirmed()
        if record.status is FileStatus.FAILED:
            raise FileNotFoundError_("Ce fichier a été invalidé.")

        # Vérifier l'objet sur S3
        meta = await self.s3.head_object(key=record.file_path)
        if meta is None:
            raise FileNotUploadedToStorage()

        actual_bytes = int(meta.get("ContentLength", 0))
        actual_kb = (actual_bytes + 1023) // 1024  # ceil KB

        # Vérifier la taille max du purpose
        _, max_kb = _max_size_for_context(record.context)
        if actual_kb > max_kb or actual_kb == 0:
            logger.warning(
                "Taille réelle %d KB > max %d KB pour %s",
                actual_kb, max_kb, record.file_path,
            )
            await self.s3.delete_object(key=record.file_path)
            record.status = FileStatus.FAILED
            await self.session.flush()
            raise FileSizeMismatch(
                declared_kb=record.size_kb_declared or 0,
                actual_kb=actual_kb,
                max_kb=max_kb,
            )

        # Valider le MIME réel (empêche les faux .webp qui sont des .exe)
        actual_mime = meta.get("ContentType", "")
        if actual_mime and actual_mime != record.mime_type:
            logger.warning(
                "MIME mismatch : déclaré=%s, réel=%s (%s)",
                record.mime_type, actual_mime, record.file_path,
            )
            await self.s3.delete_object(key=record.file_path)
            record.status = FileStatus.FAILED
            await self.session.flush()
            raise FileSizeMismatch(
                declared_kb=record.size_kb_declared or 0,
                actual_kb=actual_kb,
                max_kb=max_kb,
            )

        # Marquer comme uploadé
        record.status = FileStatus.UPLOADED
        record.size_kb_actual = actual_kb
        record.uploaded_at = utcnow()
        record.expires_at = None  # plus d'expiration (fichier légitime)
        await self.session.flush()

        # URL GET temporaire pour lecture immédiate
        read_url = await self.s3.presign_get(key=record.file_path)

        return {
            "file_id": record.id,
            "status": record.status.value,
            "size_kb": actual_kb,
            "mime_type": record.mime_type,
            "url": read_url,
            "uploaded_at": record.uploaded_at,
        }


def _max_size_for_context(context) -> tuple[str, int]:
    """Retourne (context_value, max_kb) pour un FileContext donné."""
    from app.models import FileContext

    if context is FileContext.AVATAR:
        return context.value, settings.UPLOAD_MAX_SIZE_KB_AVATAR
    return context.value, settings.UPLOAD_MAX_SIZE_KB_DOCUMENT
