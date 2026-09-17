"""Configuration centralisée de l'application.

Toutes les variables d'environnement transitent par ici — jamais d'accès
direct à `os.environ` ailleurs dans le code. `Settings` est un singleton
mis en cache via `@lru_cache` pour éviter de re-parser l'environnement
à chaque requête.
"""

from functools import lru_cache
from typing import Literal

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    PROJECT_NAME: str = "CoinDétude API"
    ENVIRONMENT: Literal["local", "staging", "production", "test"] = "local"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # --- Sécurité ---
    SECRET_KEY: str  # obligatoire, pas de valeur par défaut en dur
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 jours
    JWT_ALGORITHM: str = "HS256"

    # --- CORS (origines Flutter web / dashboard admin, etc.) ---
    BACKEND_CORS_ORIGINS: list[str] = []

    # --- Base de données ---
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "coindetude"
    POSTGRES_PASSWORD: str = "coindetude"
    POSTGRES_DB: str = "coindetude"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )

    # --- Cloudflare R2 (stockage PDF / fichiers, compatible S3) ---
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = "coindetude"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def R2_ENDPOINT_URL(self) -> str:
        return f"https://{self.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

    # --- Firebase Cloud Messaging (notifications push) ---
    FIREBASE_CREDENTIALS_PATH: str = "firebase-credentials.json"

    # --- PayGate Global (mobile money : T-Money / Flooz) ---
    PAYGATE_BASE_URL: str = "https://paygateglobal.com/api/v1"
    PAYGATE_API_KEY: str = ""
    PAYGATE_WEBHOOK_SECRET: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
