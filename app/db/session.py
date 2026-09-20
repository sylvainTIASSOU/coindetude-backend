"""Engine et session SQLAlchemy asynchrones + dépendance FastAPI `get_db`."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# `pool_pre_ping` évite les erreurs sur connexions coupées par le serveur
# (utile en particulier derrière des proxies/managed Postgres qui ferment
# les connexions idle).
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG and settings.ENVIRONMENT == "dev",
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dépendance FastAPI : une session par requête, fermée automatiquement."""
    async with AsyncSessionLocal() as session:
        yield session
