"""Service centralisé de gestion des OTP."""

from __future__ import annotations

from datetime import timedelta, timezone
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import log as logger
from app.core.security import (
    generate_otp_code,
    hash_otp_code,
    utcnow,
)
from app.models import OTPChannel, OTPCode, OTPPurpose
from app.services.otp.provider import OTPProvider, get_otp_provider
from app.services.otp.rate_limiter import OTPRateLimiter


class OTPError(Exception):
    """Erreur générique OTP."""


class OTPInvalid(OTPError):
    """Code incorrect."""


class OTPExpired(OTPError):
    """Code expiré ou inexistant."""


class OTPConsumed(OTPError):
    """Code déjà utilisé."""


class OTPTooManyAttempts(OTPError):
    """Trop de tentatives sur ce challenge."""


class OTPService:
    """Génère, envoie et vérifie les OTP."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
        provider: OTPProvider | None = None,
    ) -> None:
        self.session = session
        self.redis = redis
        self.provider = provider or get_otp_provider()
        self.rate_limiter = OTPRateLimiter(redis)

    # ------------------------------------------------------------------
    # Émission
    # ------------------------------------------------------------------

    async def create_and_send(
        self,
        *,
        phone: str,
        purpose: OTPPurpose,
        user_id: UUID | None,
        channel: OTPChannel,
        ip_address: str | None = None,
        user_agent: str | None = None,
        check_rate_limit: bool = True,
    ) -> OTPCode:
        """Crée un OTP, l'envoie via le provider, retourne la ligne créée."""
        if check_rate_limit:
            await self.rate_limiter.check_send_allowed(phone=phone, ip_address=ip_address)

        # Invalider les OTP actifs précédents pour ce (phone, purpose)
        await self._invalidate_active(phone=phone, purpose=purpose)

        code = generate_otp_code()
        ttl = (
            settings.OTP_RESET_TTL_SECONDS
            if purpose is OTPPurpose.RESET_PASSWORD
            else settings.OTP_CODE_TTL_SECONDS
        )

        otp = OTPCode(
            user_id=user_id,
            phone=phone,
            purpose=purpose,
            code_hash=hash_otp_code(code, phone, purpose.value),
            channel=channel,
            expires_at=utcnow() + timedelta(seconds=ttl),
            max_attempts=settings.OTP_MAX_ATTEMPTS,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.add(otp)
        await self.session.flush()

        # Envoi (WhatsApp prioritaire, fallback SMS si exception)
        try:
            message_id = await self.provider.send(
                phone=phone, code=code, purpose=purpose, channel=channel
            )
            otp.channel = channel
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Échec envoi %s, tentative fallback SMS : %s",
                channel.value,
                exc,
            )
            if channel is OTPChannel.WHATSAPP:
                message_id = await self.provider.send(
                    phone=phone,
                    code=code,
                    purpose=purpose,
                    channel=OTPChannel.SMS,
                )
                otp.channel = OTPChannel.SMS
            else:
                raise

        otp.provider_message_id = message_id
        await self.session.flush()

        # Expose le code en dev (ConsoleOTPProvider)
        if settings.ENVIRONMENT == "dev" or settings.OTP_FORCE_CONSOLE:
            self._last_dev_code = code  # type: ignore[attr-defined]

        return otp

    async def _invalidate_active(self, *, phone: str, purpose: OTPPurpose) -> None:
        stmt = (
            update(OTPCode)
            .where(
                OTPCode.phone == phone,
                OTPCode.purpose == purpose,
                OTPCode.consumed_at.is_(None),
            )
            .values(consumed_at=utcnow())
        )
        await self.session.execute(stmt)

    # ------------------------------------------------------------------
    # Vérification
    # ------------------------------------------------------------------

    async def verify(self, *, challenge_id: UUID, code: str) -> OTPCode:
        """Vérifie un code OTP et marque le challenge comme consommé.

        Raises:
            OTPExpired: challenge inconnu, expiré ou déjà consommé.
            OTPTooManyAttempts: attempts >= max_attempts.
            OTPInvalid: code incorrect (attempts incrémenté).
        """
        stmt = select(OTPCode).where(OTPCode.id == challenge_id)
        otp = await self.session.scalar(stmt)

        if otp is None:
            raise OTPExpired("Challenge inconnu.")

        if otp.consumed_at is not None:
            raise OTPExpired("Ce code a déjà été utilisé.")

        expires_at = otp.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at <= utcnow():
            raise OTPExpired("Ce code a expiré.")

        if otp.attempts >= otp.max_attempts:
            raise OTPTooManyAttempts("Trop de tentatives sur ce code.")

        expected = hash_otp_code(code, otp.phone, otp.purpose.value)
        if expected != otp.code_hash:
            otp.attempts += 1
            await self.session.flush()
            if otp.attempts >= otp.max_attempts:
                otp.consumed_at = utcnow()
                await self.session.flush()
                raise OTPTooManyAttempts("Trop de tentatives sur ce code.")
            raise OTPInvalid("Code incorrect.")

        # Succès
        otp.consumed_at = utcnow()
        await self.session.flush()
        return otp
