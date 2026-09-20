"""Orchestrateur des flows d'authentification (register, login, reset)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timezone
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import log as logger
from app.core.security import hash_password, mask_phone, verify_password
from app.models import (
    NotificationPreference,
    OTPChannel,
    OTPCode,
    OTPPurpose,
    ParentProfile,
    StudentProfile,
    User,
    UserRole,
)
from app.services.otp.service import OTPService
from app.services.token_service import IssuedTokens, TokenService
from app.services.trusted_device_service import TrustedDeviceService

# Sentinelle : mot de passe "bidon" pour simuler un hashage en cas d'user inexistant
_DUMMY_HASH = hash_password("dummy-timing-mitigation-1234")


@dataclass(slots=True)
class OTPSent:
    """Résultat d'une étape 1 (register/login/forgot)."""

    challenge_id: UUID
    expires_in: int
    channel: OTPChannel
    masked_phone: str
    dev_code: str | None = None  # rempli uniquement en dev


@dataclass(slots=True)
class AuthResult:
    """Résultat d'une étape 2 réussie."""

    tokens: IssuedTokens
    user: User
    trusted_device_token: str | None = None


class AuthService:
    def __init__(self, session: AsyncSession, redis: Redis) -> None:
        self.session = session
        self.redis = redis
        self.otp = OTPService(session, redis)
        self.tokens = TokenService(session, redis)
        self.devices = TrustedDeviceService(session)

    # ==================================================================
    # ÉTAPE 1 — Register
    # ==================================================================

    async def register(
        self,
        *,
        first_name: str,
        last_name: str,
        phone: str,
        email: str | None,
        password: str,
        role: UserRole,
        ip_address: str | None,
        user_agent: str | None,
    ) -> OTPSent:
        existing = await self.session.scalar(select(User).where(User.phone == phone))
        if existing and existing.phone_verified_at is not None:
            raise AuthServiceError(
                code="phone_already_used",
                detail="Un compte existe déjà avec ce numéro.",
                status_code=409,
            )

        if existing:
            # Compte non vérifié : on met à jour le password et on renvoie un OTP
            existing.first_name = first_name
            existing.last_name = last_name
            existing.email = email or existing.email
            existing.password_hash = hash_password(password)
            existing.role = role
            user = existing
        else:
            user = User(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                password_hash=hash_password(password),
                role=role,
                is_active=True,
            )
            self.session.add(user)
            await self.session.flush()
            await self._create_profile_and_preferences(user)

        # Émettre un OTP register
        channel = self._pick_channel()
        otp = await self.otp.create_and_send(
            phone=phone,
            purpose=OTPPurpose.REGISTER,
            user_id=user.id,
            channel=channel,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return self._to_otp_sent(otp, phone)

    # ==================================================================
    # ÉTAPE 1 — Login
    # ==================================================================

    async def login(
        self,
        *,
        phone: str,
        password: str,
        ip_address: str | None,
        user_agent: str | None,
        trusted_device_token: str | None,
    ) -> OTPSent | AuthResult:
        # 1. Rate limit anti-brute-force
        await self.otp.rate_limiter.check_login_allowed(phone=phone)

        user = await self.session.scalar(select(User).where(User.phone == phone))

        # Constant-time : simuler un hashage si user inexistant
        password_ok = verify_password(password, user.password_hash if user else _DUMMY_HASH)

        if user is None or not password_ok:
            raise AuthServiceError(
                code="invalid_credentials",
                detail="Téléphone ou mot de passe incorrect.",
                status_code=401,
            )
        if not user.is_active:
            raise AuthServiceError(
                code="user_disabled",
                detail="Compte suspendu.",
                status_code=403,
            )
        if user.phone_verified_at is None:
            raise AuthServiceError(
                code="phone_not_verified",
                detail="Numéro non vérifié. Utilisez /auth/resend-otp.",
                status_code=403,
            )

        # 2. Trusted device : skip OTP
        if trusted_device_token:
            trusted_user = await self.devices.validate(token=trusted_device_token, phone=phone)
            if trusted_user is not None:
                await self.otp.rate_limiter.reset_login_counter(phone=phone)
                issued = await self.tokens.issue_new_family(
                    trusted_user,
                    user_agent=user_agent,
                    ip_address=ip_address,
                )
                logger.info("Login via trusted device : user=%s", user.id)
                return AuthResult(tokens=issued, user=trusted_user)

        # 3. OTP classique
        channel = self._pick_channel()
        otp = await self.otp.create_and_send(
            phone=phone,
            purpose=OTPPurpose.LOGIN,
            user_id=user.id,
            channel=channel,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return self._to_otp_sent(otp, phone)

    # ==================================================================
    # ÉTAPE 1 — Forgot password
    # ==================================================================

    async def forgot_password(
        self, *, phone: str, ip_address: str | None, user_agent: str | None
    ) -> OTPSent:
        user = await self.session.scalar(select(User).where(User.phone == phone))
        # Anti-énumération : on ne révèle pas si le user existe
        if user is None or not user.is_active:
            # Simuler un challenge_id factice ? Non : on retourne un vrai OTP
            # "fantôme" sans user_id, ainsi la réponse est identique côté client.
            otp = await self.otp.create_and_send(
                phone=phone,
                purpose=OTPPurpose.RESET_PASSWORD,
                user_id=None,
                channel=self._pick_channel(),
                ip_address=ip_address,
                user_agent=user_agent,
            )
            return self._to_otp_sent(otp, phone)

        otp = await self.otp.create_and_send(
            phone=phone,
            purpose=OTPPurpose.RESET_PASSWORD,
            user_id=user.id,
            channel=self._pick_channel(),
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return self._to_otp_sent(otp, phone)

    # ==================================================================
    # ÉTAPE 2 — Verify OTP (register/login/reset)
    # ==================================================================

    async def verify_otp(
        self,
        *,
        challenge_id: UUID,
        code: str,
        remember_device: bool,
        user_agent: str | None,
        ip_address: str | None,
    ) -> AuthResult:
        otp = await self.otp.verify(challenge_id=challenge_id, code=code)

        if otp.user_id is None:
            # Cas forgot-password sur compte inconnu (fantôme)
            raise AuthServiceError(
                code="invalid_challenge",
                detail="Challenge invalide.",
                status_code=400,
            )

        user = await self.session.get(User, otp.user_id)
        if user is None or not user.is_active:
            raise AuthServiceError(
                code="user_not_found",
                detail="Utilisateur introuvable.",
                status_code=404,
            )

        # Vérifier le purpose
        if otp.purpose in (OTPPurpose.REGISTER, OTPPurpose.RESET_PASSWORD):
            from app.core.security import utcnow

            user.phone_verified_at = utcnow()

        # Reset password : révoquer toutes les familles existantes
        if otp.purpose is OTPPurpose.RESET_PASSWORD:
            await self.tokens.revoke_all_user_tokens(user.id)
            await self.devices.revoke_all_for_user(user.id)
            logger.info("Reset password : sessions révoquées pour user=%s", user.id)

        # Émettre une nouvelle famille
        issued = await self.tokens.issue_new_family(
            user, user_agent=user_agent, ip_address=ip_address
        )

        # Trusted device ?
        trusted_token: str | None = None
        if remember_device:
            trusted_token = await self.devices.issue(
                user=user, user_agent=user_agent, ip_address=ip_address
            )

        await self.otp.rate_limiter.reset_login_counter(phone=user.phone)

        return AuthResult(tokens=issued, user=user, trusted_device_token=trusted_token)

    # ==================================================================
    # ÉTAPE 2 — Reset password (variante de verify_otp)
    # ==================================================================

    async def reset_password(
        self,
        *,
        challenge_id: UUID,
        code: str,
        new_password: str,
        user_agent: str | None,
        ip_address: str | None,
    ) -> AuthResult:
        otp = await self.otp.verify(challenge_id=challenge_id, code=code)

        if otp.purpose is not OTPPurpose.RESET_PASSWORD:
            raise AuthServiceError(
                code="invalid_purpose",
                detail="Ce challenge n'est pas destiné à un reset password.",
                status_code=400,
            )

        user = await self.session.get(User, otp.user_id) if otp.user_id else None
        if user is None or not user.is_active:
            raise AuthServiceError(
                code="user_not_found",
                detail="Utilisateur introuvable.",
                status_code=404,
            )

        user.password_hash = hash_password(new_password)
        from app.core.security import utcnow

        user.phone_verified_at = user.phone_verified_at or utcnow()

        await self.tokens.revoke_all_user_tokens(user.id)
        await self.devices.revoke_all_for_user(user.id)

        issued = await self.tokens.issue_new_family(
            user, user_agent=user_agent, ip_address=ip_address
        )

        return AuthResult(tokens=issued, user=user)

    # ==================================================================
    # ÉTAPE 1bis — Resend OTP
    # ==================================================================

    async def resend_otp(
        self,
        *,
        challenge_id: UUID,
        ip_address: str | None,
        user_agent: str | None,
    ) -> OTPSent:
        old = await self.session.get(OTPCode, challenge_id)
        if old is None:
            raise AuthServiceError(
                code="invalid_challenge",
                detail="Challenge inconnu.",
                status_code=400,
            )
        # Réémettre pour le même (phone, purpose)
        new = await self.otp.create_and_send(
            phone=old.phone,
            purpose=old.purpose,
            user_id=old.user_id,
            channel=self._pick_channel(),
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return self._to_otp_sent(new, old.phone)

    # ==================================================================
    # Helpers
    # ==================================================================

    def _pick_channel(self) -> OTPChannel:
        return OTPChannel.WHATSAPP

    def _to_otp_sent(self, otp: OTPCode, phone: str) -> OTPSent:
        created_at = otp.created_at
        expires_at = otp.expires_at
        if created_at is not None and created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        ttl = int((expires_at - created_at).total_seconds()) if created_at else 300
        return OTPSent(
            challenge_id=otp.id,
            expires_in=ttl,
            channel=otp.channel,
            masked_phone=mask_phone(phone),
            dev_code=getattr(self.otp, "_last_dev_code", None),
        )

    async def _create_profile_and_preferences(self, user: User) -> None:
        if user.role is UserRole.STUDENT:
            import secrets as _secrets

            alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
            code = "".join(_secrets.choice(alphabet) for _ in range(6))
            self.session.add(StudentProfile(user_id=user.id, pairing_code=code))
        elif user.role is UserRole.PARENT:
            self.session.add(ParentProfile(user_id=user.id))
        self.session.add(NotificationPreference(user_id=user.id))
        await self.session.flush()


class AuthServiceError(Exception):
    """Erreur métier renvoyée aux endpoints."""

    def __init__(self, *, code: str, detail: str, status_code: int) -> None:
        self.code = code
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)
