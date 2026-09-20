from __future__ import annotations  # noqa: F404

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.db.redis import ping_redis
from app.db.session import AsyncSessionLocal

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Liveness : le process répond, sans dépendance externe."""
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness() -> JSONResponse:
    """Readiness probe : l'app peut-elle servir du trafic ?

    Vérifie :
    - Connexion PostgreSQL (SELECT 1)
    - Connexion Redis (PING)
    """
    checks: dict[str, bool] = {}

    # PostgreSQL
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        checks["postgres"] = True
    except Exception:  # noqa: BLE001
        checks["postgres"] = False

    # Redis
    checks["redis"] = await ping_redis()

    all_ok = all(checks.values())
    return JSONResponse(
        status_code=status.HTTP_200_OK if all_ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "ready" if all_ok else "not_ready", "checks": checks},
    )
