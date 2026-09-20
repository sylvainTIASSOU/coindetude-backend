"""Rate limiting Redis pour l'envoi et la vérification d'OTP."""

from __future__ import annotations

from redis.asyncio import Redis

from app.core.config import settings


class RateLimitExceeded(Exception):
    """Levée quand une limite est dépassée. ``retry_after`` en secondes."""

    def __init__(self, retry_after: int) -> None:
        self.retry_after = retry_after
        super().__init__(f"Rate limit dépassé, retry dans {retry_after}s")


class OTPRateLimiter:
    """Vérifie les quotas d'envoi OTP."""

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def _check_and_incr(
        self, key: str, limit: int, window_seconds: int
    ) -> None:
        """INCR + EXPIRE si premier. Lève RateLimitExceeded si > limit."""
        count = await self.redis.incr(key)
        if count == 1:
            await self.redis.expire(key, window_seconds)
        if count > limit:
            ttl = await self.redis.ttl(key)
            raise RateLimitExceeded(retry_after=max(ttl, 1))

    async def check_send_allowed(
        self, *, phone: str, ip_address: str | None
    ) -> None:
        """Vérifie les 3 quotas d'envoi (phone/15min, phone/jour, ip/h)."""
        await self._check_and_incr(
            f"rl:otp:send:{phone}",
            settings.OTP_MAX_SENDS_PER_15MIN,
            15 * 60,
        )
        await self._check_and_incr(
            f"rl:otp:send:{phone}:daily",
            settings.OTP_MAX_SENDS_PER_DAY,
            24 * 3600,
        )
        if ip_address:
            await self._check_and_incr(
                f"rl:otp:send:ip:{ip_address}",
                settings.OTP_MAX_SENDS_PER_IP_HOUR,
                3600,
            )

    async def check_login_allowed(self, *, phone: str) -> None:
        """Limite les tentatives de login par phone (5 / 15 min)."""
        await self._check_and_incr(f"rl:login:{phone}", 5, 15 * 60)

    async def reset_login_counter(self, *, phone: str) -> None:
        await self.redis.delete(f"rl:login:{phone}")
