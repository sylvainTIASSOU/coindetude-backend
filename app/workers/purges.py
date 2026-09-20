"""Jobs de purge et de maintenance."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from sqlalchemy import delete, select, update

from app.core.config import settings
from app.core.security import utcnow
from app.models import (
    FileStatus,
    IdempotencyKey,
    OTPCode,
    StoredFile,
    Subscription,
)

from app.core.logging import log as logger


# ---------------------------------------------------------------------------
# Purge des OTP expirés (rétention 7 jours)
# ---------------------------------------------------------------------------

async def purge_expired_otp(ctx: dict[str, Any]) -> dict[str, int]:
    """Supprime les OTP dont ``expires_at < now() - 7 jours``."""
    session_maker = ctx["session_maker"]
    cutoff = utcnow() - timedelta(days=settings.PURGE_OTP_RETENTION_DAYS)

    async with session_maker() as session:
        result = await session.execute(
            delete(OTPCode).where(OTPCode.expires_at < cutoff)
        )
        await session.commit()
        deleted = result.rowcount or 0

    logger.info("purge_expired_otp : %d OTP supprimés (cutoff=%s)", deleted, cutoff)
    return {"deleted": deleted}


# ---------------------------------------------------------------------------
# Purge des clés d'idempotence expirées
# ---------------------------------------------------------------------------

async def purge_expired_idempotency(ctx: dict[str, Any]) -> dict[str, int]:
    """Supprime les IdempotencyKey dont ``expires_at < now()``."""
    session_maker = ctx["session_maker"]
    now = utcnow()

    async with session_maker() as session:
        result = await session.execute(
            delete(IdempotencyKey).where(IdempotencyKey.expires_at < now)
        )
        await session.commit()
        deleted = result.rowcount or 0

    logger.info("purge_expired_idempotency : %d clés supprimées", deleted)
    return {"deleted": deleted}


# ---------------------------------------------------------------------------
# Purge des uploads pending orphelins (> 24h)
# ---------------------------------------------------------------------------

async def purge_pending_uploads(ctx: dict[str, Any]) -> dict[str, int]:
    """Supprime les fichiers ``pending`` expirés + leurs objets S3.

    Pour chaque orphelin :
    1. Suppression de l'objet S3 (best effort).
    2. Suppression de la row ``stored_files``.
    """
    session_maker = ctx["session_maker"]
    s3 = ctx["s3"]
    now = utcnow()

    async with session_maker() as session:
        rows = (
            await session.execute(
                select(StoredFile).where(
                    StoredFile.status == FileStatus.PENDING,
                    StoredFile.expires_at.is_not(None),
                    StoredFile.expires_at < now,
                )
            )
        ).scalars().all()

        s3_deleted = 0
        db_deleted = 0

        for row in rows:
            try:
                await s3.delete_object(key=row.file_path)
                s3_deleted += 1
            except Exception as exc:  # noqa: BLE001
                logger.warning("Suppression S3 échouée pour %s : %s", row.file_path, exc)
            await session.delete(row)
            db_deleted += 1

        await session.commit()

    logger.info(
        "purge_pending_uploads : %d rows DB, %d objets S3", db_deleted, s3_deleted
    )
    return {"db_deleted": db_deleted, "s3_deleted": s3_deleted}


# ---------------------------------------------------------------------------
# Désactivation des abonnements expirés
# ---------------------------------------------------------------------------

async def deactivate_expired_subscriptions(ctx: dict[str, Any]) -> dict[str, int]:
    """Passe ``is_active=False`` pour les abonnements dont ``end_date < now()``.

    ⚠️ N'affecte pas les abonnements freemium (``end_date IS NULL``).
    """
    session_maker = ctx["session_maker"]
    now = utcnow()

    async with session_maker() as session:
        result = await session.execute(
            update(Subscription)
            .where(
                Subscription.is_active.is_(True),
                Subscription.end_date.is_not(None),
                Subscription.end_date < now,
            )
            .values(is_active=False)
        )
        await session.commit()
        affected = result.rowcount or 0

    logger.info("deactivate_expired_subscriptions : %d abonnements désactivés", affected)
    return {"deactivated": affected}
