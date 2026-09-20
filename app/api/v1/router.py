"""Agrège tous les routers de la v1 de l'API — un seul point d'inclusion dans main.py."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, referential, sync, uploads
from app.api.v1.endpoints.admin import referential as admin_referential

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(sync.router)
api_router.include_router(uploads.router)
api_router.include_router(referential.router)
api_router.include_router(admin_referential.router)

# api_router.include_router(users.router)

# À mesure que les modules avancent, ajouter ici : referentiel, contenu,
# assistant_ia, calendrier, paiement, espace_parent, marketplace, gamification...
