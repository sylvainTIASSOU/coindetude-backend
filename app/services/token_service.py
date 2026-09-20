"""Service de gestion des refresh tokens avec rotation et détection de vol.

**Modèle de sécurité (RFC 6819 §5.2.2.3 — refresh token rotation)** :

1. À chaque login, on génère un ``family_id`` (UUID v4).
2. On crée un refresh token opaque, on stocke son SHA-256 en base.
3. Lors d'un refresh :
   a. Si le token est actif → rotation normale : révocation de l'ancien,
      création d'un nouveau dans la **même famille**.
   b. Si le token est **déjà révoqué** :
      - On vérifie dans Redis s'il existe une réponse "grâce" pour ce hash
        (fenêtre de 30 s). Si oui → on retourne **la même réponse** sans
        rien changer (idempotence pour réseau instable).
      - Sinon → **réutilisation détectée** → révocation en cascade de toute
        la famille. L'attaquant et la victime sont déconnectés.
4. ``logout`` : révoque le token courant uniquement.
5. ``logout_all`` : révoque toutes les familles de l'utilisateur.

**Grâce Redis** : clé ``refresh_grace:{sha256(token)}`` → JSON sérialisé de
``{access_token, refresh_token, expires_in}`` avec TTL 30 s. Évite les faux
positifs quand la réponse du refresh est perdue (perte réseau, retry client).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID, uuid4

from redis.asyncio import Redis
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import log as logger
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
    utcnow,
)
from app.db.redis import get_redis
from app.models import RefreshToken, User

# Fenêtre pendant laquelle un token rotaté peut être réutilisé sans sanction
GRACE_PERIOD_SECONDS = 30
GRACE_KEY_PREFIX = "refresh_grace:"


@dataclass(frozen=True, slots=True)
class IssuedTokens:
    """Paire de tokens émise par le service (retournée aux endpoints)."""

    access_token: str
    refresh_token: str
    expires_in: int  # secondes de validité de l'access_token


class TokenReuseDetected(Exception):
    """Levée quand un refresh token révoqué est réutilisé hors grâce.

    La famille entière a été révoquée. Le client doit se ré-authentifier.
    """


class TokenExpired(Exception):
    """Levée quand le refresh token est expiré côté serveur."""


class TokenInvalid(Exception):
    """Levée quand le refresh token n'existe pas ou est malformé."""


class TokenService:
    """Service d'émission, rotation et révocation des refresh tokens."""

    def __init__(self, session: AsyncSession, redis: Redis) -> None:
        self.session = session
        self.redis = redis

    # ------------------------------------------------------------------
    # Émission initiale (login)
    # ------------------------------------------------------------------

    async def issue_new_family(
        self,
        user: User,
        *,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> IssuedTokens:
        """Émet une nouvelle paire de tokens pour un login.

        Crée une nouvelle famille de refresh tokens. Utilisé au login réussi
        et à l'inscription.
        """
        family_id = uuid4()
        return await self._issue(
            user=user,
            family_id=family_id,
            user_agent=user_agent,
            ip_address=ip_address,
        )

    # ------------------------------------------------------------------
    # Rotation (refresh)
    # ------------------------------------------------------------------

    async def rotate(
        self,
        *,
        presented_token: str,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> IssuedTokens:
        """Effectue la rotation d'un refresh token.

        Gère les 4 cas :
        - Token actif → rotation normale.
        - Token rotaté récemment (dans la grâce Redis) → retourne la réponse
          mise en cache (idempotence).
        - Token révoqué hors grâce → réutilisation → révocation famille.
        - Token inconnu → ``TokenInvalid``.
        """
        token_hash = hash_refresh_token(presented_token)

        # 1. Chercher le token en base
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        db_token = await self.session.scalar(stmt)

        if db_token is None:
            logger.warning("Refresh token inconnu (hash=%s...)", token_hash[:12])
            raise TokenInvalid("Refresh token inconnu.")

        # 2. Token expiré ?
        if db_token.expires_at <= utcnow():
            raise TokenExpired("Refresh token expiré.")

        # 3. Token actif → rotation normale
        if db_token.revoked_at is None:
            return await self._rotate_active(
                db_token=db_token,
                user_agent=user_agent,
                ip_address=ip_address,
            )

        # 4. Token déjà révoqué → vérifier la grâce Redis
        grace_key = GRACE_KEY_PREFIX + token_hash
        cached = await self.redis.get(grace_key)
        if cached:
            logger.info(
                "Refresh dans la grâce (< %ds), réponse mise en cache renvoyée.",
                GRACE_PERIOD_SECONDS,
            )
            data = json.loads(cached)
            return IssuedTokens(**data)

        # 5. Réutilisation hors grâce → vol probable → révocation famille
        logger.error(
            "RÉUTILISATION de refresh token détectée (family=%s, user=%s). "
            "Révocation de toute la famille.",
            db_token.family_id,
            db_token.user_id,
        )
        await self.revoke_family(db_token.family_id)
        raise TokenReuseDetected(
            "Refresh token déjà utilisé. Toute la famille a été révoquée par mesure de sécurité."
        )

    async def _rotate_active(
        self,
        *,
        db_token: RefreshToken,
        user_agent: str | None,
        ip_address: str | None,
    ) -> IssuedTokens:
        """Rotation normale : révoque l'ancien, émet un nouveau dans la famille."""
        user = await self.session.get(User, db_token.user_id)
        if user is None or not user.is_active:
            raise TokenInvalid("Utilisateur inactif ou inexistant.")

        # Créer le nouveau token dans la même famille
        new_plain = generate_refresh_token()
        new_hash = hash_refresh_token(new_plain)
        new_token = RefreshToken(
            user_id=user.id,
            family_id=db_token.family_id,
            token_hash=new_hash,
            expires_at=utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            user_agent=user_agent,
            ip_address=ip_address,
        )
        self.session.add(new_token)
        await self.session.flush()  # récupère new_token.id

        # Révoquer l'ancien et chaîner
        db_token.revoked_at = utcnow()
        db_token.replaced_by_id = new_token.id
        await self.session.flush()

        # Créer l'access token
        access_token = create_access_token(user.id, role=user.role.value)
        issued = IssuedTokens(
            access_token=access_token,
            refresh_token=new_plain,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        # Mettre en cache la réponse pour la grâce
        await self._cache_grace(new_hash, issued)
        # Et aussi pour le token présenté (au cas où le client retente
        # avec l'ANCIEN token dans la grâce — il recevra cette même réponse)
        await self._cache_grace(db_token.token_hash, issued)

        return issued

    async def _cache_grace(self, token_hash: str, issued: IssuedTokens) -> None:
        """Stocke la réponse dans Redis pour la fenêtre de grâce."""
        key = GRACE_KEY_PREFIX + token_hash
        await self.redis.set(
            key,
            json.dumps(
                {
                    "access_token": issued.access_token,
                    "refresh_token": issued.refresh_token,
                    "expires_in": issued.expires_in,
                }
            ),
            ex=GRACE_PERIOD_SECONDS,
        )

    # ------------------------------------------------------------------
    # Révocations
    # ------------------------------------------------------------------

    async def revoke_family(self, family_id: UUID) -> int:
        """Révoque tous les tokens actifs d'une famille. Retourne le nombre."""
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.family_id == family_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=utcnow())
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount or 0 # type: ignore

    async def revoke_token(self, presented_token: str) -> bool:
        """Révoque un refresh token spécifique (logout d'un appareil).

        Retourne ``True`` si un token a été révoqué, ``False`` sinon.
        """
        token_hash = hash_refresh_token(presented_token)
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        db_token = await self.session.scalar(stmt)
        if db_token is None or db_token.revoked_at is not None:
            return False
        db_token.revoked_at = utcnow()
        await self.session.flush()
        return True

    async def revoke_all_user_tokens(self, user_id: UUID) -> int:
        """Révoque toutes les familles d'un utilisateur (logout global)."""
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=utcnow())
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount or 0 # type: ignore

    # ------------------------------------------------------------------
    # Helpers internes
    # ------------------------------------------------------------------

    async def _issue(
        self,
        *,
        user: User,
        family_id: UUID,
        user_agent: str | None,
        ip_address: str | None,
    ) -> IssuedTokens:
        """Crée un refresh token dans une famille donnée + l'access associé."""
        plain = generate_refresh_token()
        hashed = hash_refresh_token(plain)
        db_token = RefreshToken(
            user_id=user.id,
            family_id=family_id,
            token_hash=hashed,
            expires_at=utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            user_agent=user_agent,
            ip_address=ip_address,
        )
        self.session.add(db_token)
        await self.session.flush()

        access_token = create_access_token(user.id, role=user.role.value)
        return IssuedTokens(
            access_token=access_token,
            refresh_token=plain,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )


async def get_token_service(session: AsyncSession) -> TokenService:
    """Factory utilitaire (facilite les tests et l'injection FastAPI)."""
    redis = await get_redis()
    return TokenService(session=session, redis=redis)
