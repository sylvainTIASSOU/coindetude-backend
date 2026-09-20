"""Tests du endpoint /sync/apply-event."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def _auth(client: AsyncClient, phone: str = "+22890123456") -> dict:
    """Inscrit + vérifie un élève, retourne {access_token, user}."""
    r1 = await client.post("/api/v1/auth/register", json={
        "first_name": "Kofi", "last_name": "Amegan",
        "phone": phone, "password": "Sekret123",
    })
    challenge = r1.json()["challenge_id"]
    code = client.fake_otp.sent[-1][1]
    r2 = await client.post("/api/v1/auth/verify-otp", json={
        "challenge_id": challenge, "code": code,
    })
    return r2.json()


def _headers(auth: dict, idem_key: str | None = None) -> dict:
    return {
        "Authorization": f"Bearer {auth['access_token']}",
        "Idempotency-Key": idem_key or str(uuid.uuid4()),
    }


# =====================================================================
# Idempotence
# =====================================================================

async def test_same_key_same_body_returns_cached_response(
    client: AsyncClient,
) -> None:
    auth = await _auth(client, "+22890111001")
    key = str(uuid.uuid4())
    payload = {
        "entity_type": "xp_event",
        "operation": "create",
        "payload": {
            "event_id": str(uuid.uuid4()),
            "amount": 10,
            "reason": "quiz_passed",
        },
        "client_ts": _now_iso(),
    }

    r1 = await client.post(
        "/api/v1/sync/apply-event", json=payload, headers=_headers(auth, key)
    )
    r2 = await client.post(
        "/api/v1/sync/apply-event", json=payload, headers=_headers(auth, key)
    )
    assert r1.status_code == 201
    assert r2.status_code == 201
    assert r1.json() == r2.json()
    assert r2.headers.get("x-idempotent-replay") == "1"


async def test_same_key_different_body_returns_409(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111002")
    key = str(uuid.uuid4())

    r1 = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "xp_event",
            "operation": "create",
            "payload": {"event_id": str(uuid.uuid4()), "amount": 10, "reason": "a"},
            "client_ts": _now_iso(),
        },
        headers=_headers(auth, key),
    )
    assert r1.status_code == 201

    r2 = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "xp_event",
            "operation": "create",
            "payload": {"event_id": str(uuid.uuid4()), "amount": 20, "reason": "b"},
            "client_ts": _now_iso(),
        },
        headers=_headers(auth, key),
    )
    assert r2.status_code == 409
    assert r2.headers.get("x-idempotency-conflict") == "1"


async def test_missing_idempotency_key_returns_422(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111003")
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "xp_event",
            "operation": "create",
            "payload": {"event_id": str(uuid.uuid4()), "amount": 5, "reason": "x"},
            "client_ts": _now_iso(),
        },
        headers={"Authorization": f"Bearer {auth['access_token']}"},
    )
    assert r.status_code == 422


# =====================================================================
# Fenêtre client_ts
# =====================================================================

async def test_client_ts_too_old_returns_422(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111004")
    old = datetime.now(timezone.utc) - timedelta(days=8)
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "xp_event",
            "operation": "create",
            "payload": {"event_id": str(uuid.uuid4()), "amount": 5, "reason": "x"},
            "client_ts": old.isoformat(),
        },
        headers=_headers(auth),
    )
    assert r.status_code == 422


async def test_client_ts_too_future_returns_422(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111005")
    future = datetime.now(timezone.utc) + timedelta(days=8)
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "xp_event",
            "operation": "create",
            "payload": {"event_id": str(uuid.uuid4()), "amount": 5, "reason": "x"},
            "client_ts": future.isoformat(),
        },
        headers=_headers(auth),
    )
    assert r.status_code == 422


# =====================================================================
# XP events (CRDT)
# =====================================================================

async def test_xp_event_increments_total(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111006")
    event_id = str(uuid.uuid4())
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "xp_event",
            "operation": "create",
            "payload": {"event_id": event_id, "amount": 25, "reason": "quiz"},
            "client_ts": _now_iso(),
        },
        headers=_headers(auth),
    )
    assert r.status_code == 201
    assert r.json()["new_xp_total"] == 25


async def test_xp_event_dedup_by_event_id(client: AsyncClient) -> None:
    """Deux requêtes avec des Idempotency-Key différents mais même event_id."""
    auth = await _auth(client, "+22890111007")
    event_id = str(uuid.uuid4())
    base = {
        "entity_type": "xp_event",
        "operation": "create",
        "payload": {"event_id": event_id, "amount": 30, "reason": "quiz"},
        "client_ts": _now_iso(),
    }
    r1 = await client.post(
        "/api/v1/sync/apply-event", json=base, headers=_headers(auth)
    )
    r2 = await client.post(
        "/api/v1/sync/apply-event", json=base, headers=_headers(auth)
    )
    assert r1.status_code == 201
    assert r2.status_code == 200
    assert r2.json()["deduplicated"] is True


async def test_xp_event_invalid_amount_returns_422(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111008")
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "xp_event",
            "operation": "create",
            "payload": {"event_id": str(uuid.uuid4()), "amount": -5, "reason": "x"},
            "client_ts": _now_iso(),
        },
        headers=_headers(auth),
    )
    assert r.status_code == 422


# =====================================================================
# Planning tasks (LWW)
# =====================================================================

async def test_planning_create(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111009")
    task_id = str(uuid.uuid4())
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "planning_task",
            "operation": "create",
            "payload": {
                "id": task_id,
                "title": "Réviser Thalès",
                "event_type": "revision",
                "scheduled_date": _now_iso(),
                "is_completed": False,
            },
            "client_ts": _now_iso(),
        },
        headers=_headers(auth),
    )
    assert r.status_code == 201
    assert r.json()["status"] == "applied"


async def test_planning_update_lww_client_wins(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111010")
    task_id = str(uuid.uuid4())

    # Create
    await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "planning_task",
            "operation": "create",
            "payload": {
                "id": task_id, "title": "T1",
                "event_type": "revision", "scheduled_date": _now_iso(),
            },
            "client_ts": _now_iso(),
        },
        headers=_headers(auth),
    )

    # Update avec client_ts dans le futur (dans la fenêtre +7j)
    future_ts = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "planning_task",
            "operation": "update",
            "payload": {"id": task_id, "title": "T1 modifié"},
            "client_ts": future_ts,
        },
        headers=_headers(auth),
    )
    assert r.status_code == 200


async def test_planning_update_lww_server_wins(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111011")
    task_id = str(uuid.uuid4())

    # Create avec un client_ts "ancien"
    old_ts = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "planning_task",
            "operation": "create",
            "payload": {
                "id": task_id, "title": "T1",
                "event_type": "revision", "scheduled_date": old_ts,
            },
            "client_ts": old_ts,
        },
        headers=_headers(auth),
    )

    # Update avec un client_ts INFÉRIEUR à l'updated_at serveur → 409
    older_ts = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "planning_task",
            "operation": "update",
            "payload": {"id": task_id, "title": "T1 modifié"},
            "client_ts": older_ts,
        },
        headers=_headers(auth),
    )
    assert r.status_code == 409
    body = r.json()
    assert body["status"] == "conflict"
    assert body["conflict_strategy"] == "LWW"
    assert "server_state" in body


async def test_planning_delete(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111012")
    task_id = str(uuid.uuid4())
    await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "planning_task",
            "operation": "create",
            "payload": {
                "id": task_id, "title": "T1",
                "event_type": "revision", "scheduled_date": _now_iso(),
            },
            "client_ts": _now_iso(),
        },
        headers=_headers(auth),
    )
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "planning_task",
            "operation": "delete",
            "payload": {"id": task_id},
            "client_ts": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        },
        headers=_headers(auth),
    )
    assert r.status_code == 200


# =====================================================================
# Streak events (CRDT)
# =====================================================================

async def test_streak_event_first_day(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111013")
    today = datetime.now(timezone.utc).date().isoformat()
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "streak_event",
            "operation": "create",
            "payload": {"event_id": str(uuid.uuid4()), "study_date": today},
            "client_ts": _now_iso(),
        },
        headers=_headers(auth),
    )
    assert r.status_code == 201
    assert r.json()["current_streak"] == 1


async def test_streak_event_consecutive_days(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111014")
    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)

    # J-1
    r1 = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "streak_event",
            "operation": "create",
            "payload": {
                "event_id": str(uuid.uuid4()),
                "study_date": yesterday.isoformat(),
            },
            "client_ts": _now_iso(),
        },
        headers=_headers(auth),
    )
    assert r1.status_code == 201

    # Aujourd'hui → streak = 2
    r2 = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "streak_event",
            "operation": "create",
            "payload": {
                "event_id": str(uuid.uuid4()),
                "study_date": today.isoformat(),
            },
            "client_ts": _now_iso(),
        },
        headers=_headers(auth),
    )
    assert r2.json()["current_streak"] == 2


async def test_streak_event_dedup_by_event_id(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111015")
    today = datetime.now(timezone.utc).date().isoformat()
    event_id = str(uuid.uuid4())
    base = {
        "entity_type": "streak_event",
        "operation": "create",
        "payload": {"event_id": event_id, "study_date": today},
        "client_ts": _now_iso(),
    }
    await client.post(
        "/api/v1/sync/apply-event", json=base, headers=_headers(auth)
    )
    r2 = await client.post(
        "/api/v1/sync/apply-event", json=base, headers=_headers(auth)
    )
    assert r2.status_code == 200
    assert r2.json()["deduplicated"] is True


# =====================================================================
# Erreurs
# =====================================================================

async def test_unknown_entity_type_returns_422(client: AsyncClient) -> None:
    auth = await _auth(client, "+22890111016")
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "unknown_entity",
            "operation": "create",
            "payload": {},
            "client_ts": _now_iso(),
        },
        headers=_headers(auth),
    )
    assert r.status_code == 422


async def test_unauthenticated_returns_401(client: AsyncClient) -> None:
    r = await client.post(
        "/api/v1/sync/apply-event",
        json={
            "entity_type": "xp_event",
            "operation": "create",
            "payload": {"event_id": str(uuid.uuid4()), "amount": 5, "reason": "x"},
            "client_ts": _now_iso(),
        },
        headers={"Idempotency-Key": str(uuid.uuid4())},
    )
    assert r.status_code == 401
