"""Tests pour le schéma OpenAPI enrichi et les endpoints de contrat."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from httpx import AsyncClient

from app.core.openapi import OPENAPI_SERVERS
from scripts.export_openapi import check_openapi_drift, generate_openapi_dict


@pytest.mark.asyncio
async def test_openapi_endpoints_return_200(client: AsyncClient) -> None:
    """Vérifie que les endpoints /api/v1/openapi.json et /openapi.json répondent 200."""
    # 1. Endpoint standard sous préfixe API
    resp_v1 = await client.get("/api/v1/openapi.json")
    assert resp_v1.status_code == 200
    data_v1 = resp_v1.json()

    # 2. Endpoint miroir à la racine
    resp_root = await client.get("/openapi.json")
    assert resp_root.status_code == 200
    data_root = resp_root.json()

    # Les deux doivent être strictement identiques
    assert data_v1 == data_root


def test_openapi_metadata_enrichment() -> None:
    """Vérifie que le schéma OpenAPI contient les métadonnées enrichies."""
    schema = generate_openapi_dict()

    # Infos générales
    assert "info" in schema
    assert schema["info"]["title"] == "CoinDétude API"
    assert "contact" in schema["info"]
    assert schema["info"]["contact"]["email"] == "contact@coindetude.tg"
    assert "license" in schema["info"]

    # Serveurs configurés
    assert "servers" in schema
    assert len(schema["servers"]) == len(OPENAPI_SERVERS)
    server_urls = [s["url"] for s in schema["servers"]]
    assert "/" in server_urls or "https://coindetude-backend.fastapicloud.dev" in server_urls
    assert "https://api.coindetude.tg" in server_urls

    # Tags thématiques ordonnés
    assert "tags" in schema
    tag_names = [t["name"] for t in schema["tags"]]
    for expected in ["auth", "referential", "sync", "uploads", "admin:referential", "health"]:
        assert expected in tag_names

    # x-tagGroups pour Redoc
    assert "x-tagGroups" in schema
    group_names = [g["name"] for g in schema["x-tagGroups"]]
    assert "Authentification & Sécurité" in group_names
    assert "Pédagogie & Contenus" in group_names


def test_openapi_security_schemes() -> None:
    """Vérifie la présence du schéma BearerAuth et son association aux routes protégées."""
    schema = generate_openapi_dict()

    components = schema.get("components", {})
    security_schemes = components.get("securitySchemes", {})

    # BearerAuth doit être déclaré
    assert "BearerAuth" in security_schemes
    assert security_schemes["BearerAuth"]["type"] == "http"
    assert security_schemes["BearerAuth"]["scheme"] == "bearer"
    assert security_schemes["BearerAuth"]["bearerFormat"] == "JWT"

    paths = schema.get("paths", {})

    # Vérifier un endpoint protégé par CurrentUser : /api/v1/sync/apply-event
    sync_op = paths.get("/api/v1/sync/apply-event", {}).get("post", {})
    assert "security" in sync_op
    security_reqs = sync_op["security"]
    assert any("BearerAuth" in req for req in security_reqs)

    # Vérifier un endpoint protégé par AdminUser : /api/v1/admin/referential/levels (POST)
    admin_op = paths.get("/api/v1/admin/referential/levels", {}).get("post", {})
    assert "security" in admin_op
    assert any("BearerAuth" in req for req in admin_op["security"])


def test_openapi_export_drift_check(tmp_path: Path) -> None:
    """Vérifie le fonctionnement de check_openapi_drift."""
    temp_file = tmp_path / "test_openapi.json"

    # Fichier inexistant -> False
    assert check_openapi_drift(temp_file) is False

    # Écriture du schéma valide
    schema = generate_openapi_dict()
    temp_file.write_text(json.dumps(schema), encoding="utf-8")
    assert check_openapi_drift(temp_file) is True

    # Dérive artificielle
    corrupted_schema = dict(schema)
    corrupted_schema["info"] = {"title": "Drifted"}
    temp_file.write_text(json.dumps(corrupted_schema), encoding="utf-8")
    assert check_openapi_drift(temp_file) is False
