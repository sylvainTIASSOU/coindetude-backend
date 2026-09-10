"""Endpoints de santé — utilisés par les probes Docker/K8s et le monitoring."""

from fastapi import APIRouter
from sqlalchemy import text

from app.api.deps import DbSession

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Liveness : le process répond, sans dépendance externe."""
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness(db: DbSession) -> dict[str, str]:
    """Readiness : vérifie que la base de données est joignable."""
    await db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}
