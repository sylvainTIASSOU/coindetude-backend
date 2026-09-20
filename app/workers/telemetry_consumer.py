"""Consumer de la queue Redis ``telemetry:queue`` → PostHog /batch.

**Fonctionnement** :

1. Pop jusqu'à ``TELEMETRY_CONSUMER_BATCH_SIZE`` items de ``telemetry:queue``.
2. Regroupe les events par ``user_id`` (PostHog aime bien un batch homogène).
3. POST vers ``{POSTHOG_URL}/batch/`` avec la clé personnelle.
4. En cas d'échec après ``MAX_RETRIES``, push dans ``telemetry:dlq`` (dead letter).

**Idempotence** : chaque item contient un ``request_id`` unique. PostHog
déduplique en interne par ``(event, distinct_id, timestamp)`` si configuré.
Sinon, la queue vidée après un POST réussi garantit au-moins-une-fois.
"""

from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import settings

from app.core.logging import log as logger


def _posthog_batch_url() -> str:
    if settings.TELEMETRY_POSTHOG_BATCH_URL:
        return settings.TELEMETRY_POSTHOG_BATCH_URL
    base = settings.POSTHOG_URL.rstrip("/") # type: ignore
    return f"{base}/batch/"


def _to_posthog_event(
    event: dict[str, Any], *, distinct_id: str, country_code: str | None
) -> dict[str, Any]:
    """Transforme un event interne en event PostHog."""
    properties = dict(event.get("properties", {}))
    properties.setdefault("$lib", "coindetude-backend")
    properties.setdefault("$lib_version", settings.APP_VERSION)
    if country_code:
        properties.setdefault("country_code", country_code)
    if event.get("request_id"):
        properties.setdefault("request_id", event["request_id"])
    return {
        "event": event["event"],
        "distinct_id": distinct_id,
        "properties": properties,
        "timestamp": event["timestamp"],
    }


async def send_batch_to_posthog(
    http: httpx.AsyncClient,
    *,
    events: list[dict[str, Any]],
    user_id: str,
    country_code: str | None = None,
) -> tuple[bool, str | None]:
    """POST un batch vers PostHog. Retourne ``(success, error_msg)``.

    ⚠️ Si PostHog désactivé (``POSTHOG_ENABLED=False``), on log et on
    considère le batch comme traité (pas de retry inutile en dev).
    """
    if not settings.POSTHOG_ENABLED or not settings.POSTHOG_URL:
        logger.info(
            "[MOCK] PostHog batch de %d events pour user=%s",
            len(events), user_id,
        )
        return True, None

    payload = {
        "api_key": settings.POSTHOG_PERSONAL_API_KEY,
        "historical_migration": False,
        "batch": [
            _to_posthog_event(e, distinct_id=user_id, country_code=country_code)
            for e in events
        ],
    }
    try:
        resp = await http.post(
            _posthog_batch_url(),
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        return True, None
    except httpx.HTTPError as exc:
        return False, str(exc)


async def telemetry_consumer(ctx: dict[str, Any]) -> dict[str, int]:
    """Job ARQ : drain la queue telemetry (appelé toutes les minutes)."""
    from app.core.config import settings

    redis = ctx["redis"]
    http = ctx["http"]

    stats = {"processed": 0, "sent": 0, "failed": 0, "requeued": 0, "dlq": 0}

    # Pop jusqu'à BATCH_SIZE items (bloquant non : on prend ce qui est dispo)
    items = await redis.lrange(
        settings.TELEMETRY_QUEUE_KEY, 0, settings.TELEMETRY_CONSUMER_BATCH_SIZE - 1
    )
    if not items:
        return stats

    # Retirer immédiatement de la queue (on remettra en cas d'échec)
    await redis.ltrim(
        settings.TELEMETRY_QUEUE_KEY,
        len(items),
        -1,
    )

    for raw in items:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            logger.error("Item telemetry corrompu, DLQ")
            await redis.lpush(settings.TELEMETRY_DLQ_KEY, raw)
            stats["dlq"] += 1
            continue

        stats["processed"] += 1
        user_id = parsed.get("user_id", "unknown")
        events = parsed.get("events", [])
        if not events:
            continue

        ok, err = await send_batch_to_posthog(
            http,
            events=events,
            user_id=user_id,
            country_code=events[0].get("country_code"),
        )
        if ok:
            stats["sent"] += 1
            continue

        # Retry : on ré-empile en fin de queue (re-tenté au prochain run)
        retries = parsed.get("retries", 0) + 1
        if retries >= settings.TELEMETRY_CONSUMER_MAX_RETRIES:
            logger.error(
                "Telemetry item échoué %d fois, DLQ : %s", retries, err
            )
            await redis.lpush(settings.TELEMETRY_DLQ_KEY, raw)
            stats["dlq"] += 1
        else:
            parsed["retries"] = retries
            parsed["last_error"] = err
            # Backoff : on repousse en fin de queue pour ne pas boucler
            await redis.rpush(
                settings.TELEMETRY_QUEUE_KEY, json.dumps(parsed, default=str)
            )
            stats["requeued"] += 1

    logger.info("Telemetry consumer : %s", stats)
    return stats
