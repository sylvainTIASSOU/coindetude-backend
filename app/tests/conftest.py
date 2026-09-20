"""Fixtures partagées : DB isolée par test + client HTTP asynchrone.

Utilise SQLite en mémoire pour la vitesse. Attention : certains types
PostgreSQL avancés (JSONB, ARRAY, ENUM natif...) ne se comportent pas
à l'identique sous SQLite — pour les tests touchant ces colonnes,
préférer un vrai Postgres de test (voir docker-compose, service `db`,
avec une base `coindetude_test` dédiée).
"""

from collections.abc import AsyncGenerator
import os
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.pool import StaticPool

# Les tests utilisent l'application sans dépendre d'une clé du shell local.
if len(os.environ.get("SECRET_KEY", "")) < 32:
    os.environ["SECRET_KEY"] = "test-secret-key-for-pytest-only-32-chars"

from app.models.base import Base
from app.db.session import get_db
from app.main import app
from app.services.otp.provider import OTPProvider


class FakeOTPProvider(OTPProvider):
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    async def send(self, *, phone: str, code: str, purpose, channel) -> str:  # type: ignore[no-untyped-def]
        self.sent.append((phone, code))
        return f"fake-{len(self.sent)}"


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, Any] = {}
        self.ttls: dict[str, int] = {}

    async def incr(self, key: str) -> int:
        self.values[key] = int(self.values.get(key, 0)) + 1
        return self.values[key]

    async def expire(self, key: str, seconds: int) -> bool:
        self.ttls[key] = seconds
        return True

    async def ttl(self, key: str) -> int:
        return self.ttls.get(key, -1)

    async def delete(self, key: str) -> int:
        existed = key in self.values
        self.values.pop(key, None)
        self.ttls.pop(key, None)
        return int(existed)

    async def set(self, key: str, value: Any, *, nx: bool = False, ex: int | None = None) -> bool:
        if nx and key in self.values:
            return False
        self.values[key] = value
        if ex is not None:
            self.ttls[key] = ex
        return True


@compiles(JSONB, "sqlite")
def _compile_jsonb_for_sqlite(type_, compiler, **kw):  # type: ignore[no-untyped-def]
    return "JSON"


def _remove_duplicate_indexes() -> None:
    for table in Base.metadata.tables.values():
        seen_names: set[str] = set()
        for index in list(table.indexes):
            if index.name in seen_names:
                table.indexes.remove(index)
            else:
                seen_names.add(index.name)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        _remove_duplicate_indexes()
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with session_maker() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def client(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncGenerator[AsyncClient, None]:
    fake_otp = FakeOTPProvider()
    fake_redis = FakeRedis()
    monkeypatch.setattr("app.services.otp.service.get_otp_provider", lambda: fake_otp)

    async def _get_fake_redis() -> FakeRedis:
        return fake_redis

    monkeypatch.setattr("app.api.v1.endpoints.auth.get_redis", _get_fake_redis)
    monkeypatch.setattr("app.api.v1.endpoints.sync.get_redis", _get_fake_redis)

    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        ac.fake_otp = fake_otp  # type: ignore[attr-defined]
        yield ac
    app.dependency_overrides.clear()
