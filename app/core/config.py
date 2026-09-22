"""Configuration centralisée de l'application.

Toutes les variables d'environnement transitent par ici — jamais d'accès
direct à `os.environ` ailleurs dans le code. `Settings` est un singleton
mis en cache via `@lru_cache` pour éviter de re-parser l'environnement
à chaque requête.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- Application ---
    PROJECT_NAME: str = "CoinDétude API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["dev", "staging", "prod"] = "dev"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # --- Sécurité ---
    SECRET_KEY: str = Field(..., min_length=32)  # obligatoire, pas de valeur par défaut en dur
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # 24h
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30  # 7 jours
    JWT_ALGORITHM: str = "HS256"

    # --- CORS (origines Flutter web / dashboard admin, etc.) ---
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # --- Base de données ---
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "coindetude"
    POSTGRES_PASSWORD: str = "coindetude"
    POSTGRES_DB: str = "coindetude"
    DATABASE_URL: str = ""  # construit dynamiquement si non fourni
    # @computed_field  # type: ignore[prop-decorator]
    # @property
    # def DATABASE_URL(self) -> str:
    #     return str(
    #         PostgresDsn.build(
    #             scheme="postgresql+asyncpg",
    #             username=self.POSTGRES_USER,
    #             password=self.POSTGRES_PASSWORD,
    #             host=self.POSTGRES_SERVER,
    #             port=self.POSTGRES_PORT,
    #             path=self.POSTGRES_DB,
    #         )
    #     )

    # --- Redis ---
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_USER: str = "user"

    # --- Uploads ---
    UPLOAD_MAX_SIZE_KB_DOCUMENT: int = 500
    UPLOAD_MAX_SIZE_KB_AVATAR: int = 150
    UPLOAD_ALLOWED_MIME_TYPES: list[str] = [
        "image/webp",
        "image/jpeg",
        "application/pdf",
    ]
    UPLOAD_PRESIGN_TTL_SECONDS: int = 900  # 15 min
    UPLOAD_GET_TTL_SECONDS: int = 3600  # 1 h pour la lecture
    UPLOAD_PENDING_TTL_HOURS: int = 24  # purge différée
    S3_AUTO_CREATE_BUCKET_IN_DEV: bool = True  # crée le bucket au démarrage

    # --- Worker ARQ ---
    WORKER_ENABLED: bool = True
    WORKER_REDIS_DB: int = 1  # DB Redis dédiée au broker ARQ
    WORKER_MAX_JOBS: int = 10
    WORKER_JOB_TIMEOUT_SECONDS: int = 300  # 5 min max par job
    WORKER_KEEP_RESULT_SECONDS: int = 3600  # 1h de rétention des résultats

    # --- Telemetry consumer ---
    POSTHOG_URL: str = ""
    POSTHOG_PERSONAL_API_KEY: str = ""
    POSTHOG_ENABLED: bool = False
    TELEMETRY_QUEUE_KEY: str = "telemetry:queue"
    TELEMETRY_DLQ_KEY: str = "telemetry:dlq"
    TELEMETRY_CONSUMER_BATCH_SIZE: int = 100  # events par pop
    TELEMETRY_CONSUMER_MAX_RETRIES: int = 3
    TELEMETRY_POSTHOG_BATCH_URL: str = ""  # si vide : {POSTHOG_URL}/batch/

    # --- Purges ---
    PURGE_OTP_RETENTION_DAYS: int = 7
    PURGE_PENDING_UPLOADS_HOURS: int = 24
    SUBSCRIPTION_CHECK_INTERVAL_MINUTES: int = 15

    # REDIS_URL: str = ""  # construit dynamiquement si non fourni

    @computed_field  # type: ignore[prop-decorator]
    @property
    def REDIS_URL(self) -> str:
        """URL Redis complète."""
        # auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # --- Cloudflare R2 (stockage PDF / fichiers, compatible S3) ---
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = "coindetude"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def R2_ENDPOINT_URL(self) -> str:
        return f"https://{self.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

    # --- Seed automatique ---
    # Si True, le seed pédagogique + plans est lancé en arrière-plan au démarrage
    # (uniquement s'il n'a pas déjà été exécuté, contrôlé par une clé Redis).
    AUTO_SEED_ENABLED: bool = True
    AUTO_SEED_LOCK_TTL_SECONDS: int = 300  # 5 min (anti-concurrence multi-worker)

    # --- Firebase Cloud Messaging (notifications push) ---
    FIREBASE_CREDENTIALS_PATH: str = "firebase-credentials.json"

    # --- PayGate Global (mobile money : T-Money / Flooz) ---
    PAYGATE_BASE_URL: str = "https://paygateglobal.com/api/v1"
    PAYGATE_API_KEY: str = ""
    PAYGATE_WEBHOOK_SECRET: str = ""

    # --- Stockage objet (S3/MinIO/R2) ---
    S3_ENDPOINT_URL: str | None = None  # ex: http://minio:9000 en dev
    S3_ACCESS_KEY_ID: str = ""
    S3_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = "coindetude"
    S3_REGION: str = "auto"
    S3_PRESIGN_EXPIRE_SECONDS: int = 900  # 15 min

    # --- OTP / SMS / WhatsApp ---
    OTP_CODE_TTL_SECONDS: int = 300  # 5 min (register/login)
    OTP_RESET_TTL_SECONDS: int = 600  # 10 min (reset password)
    OTP_MAX_ATTEMPTS: int = 5
    OTP_MAX_SENDS_PER_15MIN: int = 3
    OTP_MAX_SENDS_PER_DAY: int = 10
    OTP_MAX_SENDS_PER_IP_HOUR: int = 20
    TRUSTED_DEVICE_TTL_DAYS: int = 30

    # Africa's Talking
    AT_USERNAME: str = "sandbox"
    AT_API_KEY: str = ""
    AT_SENDER_ID: str = "CoinDetude"
    AT_WHATSAPP_SENDER: str | None = None  # ex: "22890000000"
    OTP_FORCE_CONSOLE: bool = False  # True = code dans la réponse HTTP (dev)

    # --- Observabilité ---
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    SENTRY_DSN: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


settings = get_settings()
