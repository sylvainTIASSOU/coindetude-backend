"""Exceptions du module sync."""

from __future__ import annotations

from typing import Any

from app.models.enums import ConflictStrategy


class SyncError(Exception):
    """Erreur générique de sync."""

    def __init__(self, detail: str, status_code: int = 400) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class ClientTimestampOutOfWindow(SyncError):
    """``client_ts`` hors fenêtre ±7 jours."""

    def __init__(self) -> None:
        super().__init__(
            detail="client_ts doit être dans les ±7 jours autour de maintenant.",
            status_code=422,
        )


class IdempotencyKeyConflict(SyncError):
    """Même ``Idempotency-Key`` mais body différent."""

    def __init__(self) -> None:
        super().__init__(
            detail="Cette Idempotency-Key a déjà été utilisée avec un body différent.",
            status_code=409,
        )


class IdempotencyInFlight(SyncError):
    """Une requête avec la même clé est en cours de traitement."""

    def __init__(self, retry_after: int = 2) -> None:
        super().__init__(
            detail="Une requête avec cette Idempotency-Key est déjà en cours.",
            status_code=409,
        )
        self.retry_after = retry_after


class ConflictDetected(Exception):
    """Conflit métier (LWW ou MANUAL)."""

    def __init__(
        self,
        *,
        server_state: dict[str, Any],
        strategy: ConflictStrategy,
    ) -> None:
        self.server_state = server_state
        self.strategy = strategy
        super().__init__(f"Conflit détecté (stratégie {strategy.value})")
