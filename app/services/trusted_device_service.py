"""Service des appareils de confiance (skip OTP pendant 30j)."""

from __future__ import annotations

from datetime import timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    generate_refresh_token,
    hash_refresh_token,
    utcnow,
)
from app.models import TrustedDevice, User


class TrustedDeviceService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def issue(
        self,
        *,
        user: User,
        user_agent: str | None,
        ip_address: str | None,
        device_name: str | None = None,
    ) -> str:
        """Émet un token trusted device (retourné en clair une seule fois)."""
        plain = generate_refresh_token()
        device = TrustedDevice(
            user_id=user.id,
            token_hash=hash_refresh_token(plain),
            device_name=device_name,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=utcnow() + timedelta(days=settings.TRUSTED_DEVICE_TTL_DAYS),
        )
        self.session.add(device)
        await self.session.flush()
        return plain

    async def validate(self, *, token: str, phone: str) -> User | None:
        """Retourne l'utilisateur si le token est valide et lié au phone."""
        if not token:
            return None
        token_hash = hash_refresh_token(token)
        stmt = select(TrustedDevice).where(TrustedDevice.token_hash == token_hash)
        device = await self.session.scalar(stmt)
        if device is None or not device.is_valid:
            return None

        user = await self.session.get(User, device.user_id)
        if user is None or user.phone != phone or not user.is_active:
            return None

        # Rafraîchir last_used_at
        device.last_used_at = utcnow()
        await self.session.flush()
        return user

    async def revoke_all_for_user(self, user_id: UUID) -> int:
        """Révoque tous les trusted devices (appelé par /logout-all)."""
        from sqlalchemy import delete

        stmt = delete(TrustedDevice).where(TrustedDevice.user_id == user_id)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount or 0 # type: ignore
