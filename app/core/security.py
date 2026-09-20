"""Primitives de sécurité : hash de mot de passe, JWT, tokens opaques.

- **Mots de passe** : Argon2id (hash lent, résistant GPU).
- **Access tokens** : JWT HS256 signés par ``SECRET_KEY``.
- **Refresh tokens** : chaînes opaques aléatoires (256 bits), stockées
  en base uniquement sous forme de hash SHA-256 hexadécimal.
- **Comparaison** : ``secrets.compare_digest`` (constant-time).
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

import jwt
from passlib.context import CryptContext
import hmac
import hashlib
from app.core.config import settings

# Argon2id : recommandation OWASP 2024
_pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__type="ID",       # Argon2id
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,
    argon2__parallelism=4,
)


# ---------------------------------------------------------------------------
# Mots de passe
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """Hash un mot de passe avec Argon2id."""
    return _pwd_context.hash(password) # type: ignore


def verify_password(plain: str, hashed: str) -> bool:
    """Vérifie un mot de passe (constant-time via passlib)."""
    try:
        return _pwd_context.verify(plain, hashed) # type: ignore
    except Exception:  # noqa: BLE001
        return False

def generate_otp_code() -> str:
    """Génère un code OTP à 6 chiffres (CSPRNG), padding à gauche."""
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp_code(code: str, phone: str, purpose: str) -> str:
    """HMAC-SHA256(code, SECRET_KEY + phone + purpose).

    Le phone et le purpose sont inclus pour empêcher qu'un code valide pour
    un couple (phone, purpose) soit valide pour un autre.
    """
    msg = f"{phone}:{purpose}:{code}".encode("utf-8")
    return hmac.new(
        settings.SECRET_KEY.encode("utf-8"), msg, hashlib.sha256
    ).hexdigest()


def mask_phone(phone: str) -> str:
    """Masque un numéro pour l'affichage : +22890123*** → +228*****23."""
    if len(phone) <= 6:
        return phone
    return f"{phone[:4]}****{phone[-2:]}"

# ---------------------------------------------------------------------------
# Access tokens (JWT)
# ---------------------------------------------------------------------------

def create_access_token(
    subject: str | UUID,
    *,
    role: str | None = None,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Crée un JWT d'accès.

    Claims standards :
    - ``sub`` : identifiant utilisateur (str).
    - ``exp`` : expiration.
    - ``iat`` : émission.
    - ``jti`` : identifiant unique du JWT.
    - ``typ`` : toujours ``"access"`` (empêche la confusion avec refresh).
    - ``role`` : rôle applicatif (student, parent...).
    """
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ))
    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "jti": str(uuid4()),
        "typ": "access",
    }
    if role is not None:
        payload["role"] = role
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Décode et valide un access token.

    Raises:
        jwt.ExpiredSignatureError: token expiré.
        jwt.InvalidTokenError: token invalide (signature, format, typ).
    """
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        options={"require": ["exp", "sub", "jti", "typ"]},
    )
    if payload.get("typ") != "access":
        raise jwt.InvalidTokenError("Type de token invalide (attendu: access)")
    return payload


# ---------------------------------------------------------------------------
# Refresh tokens (opaques, hashés en base)
# ---------------------------------------------------------------------------

def generate_refresh_token() -> str:
    """Génère un refresh token opaque (32 octets → 43 chars base64url)."""
    return secrets.token_urlsafe(32)


def hash_refresh_token(token: str) -> str:
    """Retourne le SHA-256 hexadécimal (64 chars) d'un refresh token.

    SHA-256 plutôt qu'Argon2 : les refresh tokens ont une entropie de 256 bits,
    donc un hash rapide suffit. Argon2 ralentirait chaque refresh de ~100 ms
    sans gain réel de sécurité.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def constant_time_equals(a: str, b: str) -> bool:
    """Comparaison à temps constant (résiste aux timing attacks)."""
    return secrets.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


def utcnow() -> datetime:
    """Retourne l'instant courant UTC (aware)."""
    return datetime.now(timezone.utc)
