"""Configuration OpenAPI enrichie pour CoinDétude.

Centralise les métadonnées de l'API, les tags hiérarchisés, les serveurs,
les schémas de sécurité (Bearer JWT) et la personnalisation des Operation IDs
pour la génération optimale du SDK Dart/Flutter (dart-dio).
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

from app.core.config import settings

# --- Métadonnées des Tags OpenAPI ---
OPENAPI_TAGS: list[dict[str, Any]] = [
    {
        "name": "auth",
        "description": (
            "**Authentification & Sessions** — Enregistrement, challenge OTP par SMS "
            "ou WhatsApp, connexion par mot de passe, rafraîchissement des tokens JWT, "
            "déconnexion et gestion des appareils de confiance."
        ),
    },
    {
        "name": "referential",
        "description": (
            "**Référentiel Pédagogique Public** — Consultation en lecture seule des cycles "
            "officiels togolais (Primaire, Collège, Lycée), des niveaux (CEPD, BEPC, BAC), "
            "des séries, des matières, des chapitres et des fiches ressources. "
            "Mis en cache distribué Redis avec headers HTTP Cache-Control."
        ),
    },
    {
        "name": "sync",
        "description": (
            "**Synchronisation Offline-First** — Réplication des mutations effectuées "
            "hors-ligne sur l'application mobile Flutter (progression, tâches de révision). "
            "Garantie d'idempotence stricte via le header `Idempotency-Key` (UUID v4)."
        ),
    },
    {
        "name": "uploads",
        "description": (
            "**Uploads & Stockage d'Objets** — Négociation d'URLs pré-signées "
            "(S3 / Cloudflare R2) pour l'upload direct de binaires (avatars, documents, PDF) "
            "sans saturer la bande passante du backend, suivi de la confirmation d'intégrité."
        ),
    },
    {
        "name": "admin:referential",
        "description": (
            "**Administration du Référentiel** — Opérations CRUD complètes sur les niveaux, "
            "séries, matières, chapitres et ressources pédagogiques. "
            "Strictement réservé aux utilisateurs ayant le rôle `admin`."
        ),
    },
    {
        "name": "health",
        "description": (
            "**Santé & Observabilité** — Probes de liveness (`/health`) et de readiness "
            "(`/health/ready` vérifiant les connexions actives PostgreSQL et Redis)."
        ),
    },
]

# --- Regroupement des tags pour Redoc (x-tagGroups) ---
OPENAPI_TAG_GROUPS: list[dict[str, Any]] = [
    {
        "name": "Authentification & Sécurité",
        "tags": ["auth"],
    },
    {
        "name": "Pédagogie & Contenus",
        "tags": ["referential", "admin:referential"],
    },
    {
        "name": "Offline & Fichiers",
        "tags": ["sync", "uploads"],
    },
    {
        "name": "Système & Observabilité",
        "tags": ["health"],
    },
]

# --- Environnements / Serveurs ---
OPENAPI_SERVERS: list[dict[str, str]] = [
    {
        "url": settings.PUBLIC_API_URL,
        "description": "Serveur API courant",
    },
    {
        "url": "https://staging-api.coindetude.tg",
        "description": "Environnement de recette (Staging)",
    },
    {
        "url": "https://api.coindetude.tg",
        "description": "Environnement de production",
    },
]

# --- Description Markdown complète de l'API ---
OPENAPI_DESCRIPTION = """
## Bienvenue sur l'API CoinDétude 🇹🇬

**CoinDétude** est la plateforme éducative d'accompagnement et de révision scolaire
pour les élèves togolais préparant les examens nationaux (**CEPD, BEPC, BAC 1 & 2**).

### Architecture & Principes Directeurs
1. **Frugalité Réseau & Offline-First** :
   - L'application mobile Flutter fonctionne en mode déconnecté.
   - Les mutations différées sont poussées vers `/api/v1/sync/apply-event`
     avec un header `Idempotency-Key` (UUIDv4).
   - Les fichiers ne transitent jamais directement par le backend :
     upload direct via URLs présignées S3/R2.
2. **Authentification Hybride Robuste** :
   - Identifiant principal : Numéro de téléphone au format international (`+228XXXXXXXX`).
   - OTP par SMS ou WhatsApp pour la validation de compte et réinitialisation de mot de passe.
   - Sessions basées sur des tokens JWT courts (15 min) et des refresh tokens révocables (30 jours).
3. **Sécurité & Contrôle d'Accès** :
   - Fournir le token d'accès dans le header : `Authorization: Bearer <access_token>`.
   - Rôles stricts : `student`, `parent`, `tutor`, `admin`.

### Format des Erreurs Standard
Toutes les erreurs renvoient une charge utile JSON standard :
```json
{
  "detail": "Message explicatif de l'erreur ou liste des erreurs de validation"
}
```
"""


def custom_generate_unique_id(route: APIRoute) -> str:
    """Génère un Operation ID épuré et idiomatique pour le SDK Dart.

    Permet à openapi-generator (dart-dio) de nommer les méthodes de façon propre :
    - `authApi.login(...)` au lieu de `authApi.loginApiV1AuthLoginPost(...)`
    - `referentialApi.listLevels(...)`
    - `syncApi.applyEvent(...)`
    """
    if route.operation_id:
        return route.operation_id
    # Si la route n'a pas d'operation_id explicite, utiliser son nom de fonction
    return route.name


def custom_openapi_factory(app: FastAPI) -> dict[str, Any]:
    """Génère le schéma OpenAPI enrichi avec sécurité, tags et exemples."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.APP_VERSION,
        summary="API backend pour la plateforme scolaire CoinDétude",
        description=OPENAPI_DESCRIPTION,
        routes=app.routes,
        tags=OPENAPI_TAGS,
        servers=OPENAPI_SERVERS,
    )

    # 1. Ajout de l'extension x-tagGroups pour Redoc / documentation interactive
    openapi_schema["x-tagGroups"] = OPENAPI_TAG_GROUPS

    # 2. Informations de contact et licence
    openapi_schema["info"]["contact"] = {
        "name": "Support Technique CoinDétude",
        "email": "contact@coindetude.tg",
        "url": "https://coindetude-backend.fastapicloud.dev",
    }
    openapi_schema["info"]["license"] = {
        "name": "Proprietary - CoinDétude",
        "url": "https://coindetude-backend.fastapicloud.dev/terms",
    }

    # 3. Enrichissement des Security Schemes
    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})

    # Ajout du schéma HTTP Bearer (standard pour les SDKs Dio / Flutter)
    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": (
            "Entrez votre JWT sous la forme : `Bearer <access_token>`.\n"
            "Obtenu via `POST /api/v1/auth/verify-otp` ou `POST /api/v1/auth/refresh`."
        ),
    }

    # 4. Harmonisation de la sécurité sur les opérations protégées
    # Si une opération a déjà OAuth2PasswordBearer, on lui associe aussi BearerAuth
    paths = openapi_schema.get("paths", {})
    for path_item in paths.values():
        for method, operation in path_item.items():
            if method.lower() in ("get", "post", "put", "patch", "delete"):
                sec = operation.get("security", [])
                if sec:
                    # S'il y a déjà une sécurité (ex: OAuth2PasswordBearer),
                    # on s'assure que BearerAuth est inclus
                    has_bearer = any("BearerAuth" in s for s in sec)
                    if not has_bearer:
                        sec.append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema
