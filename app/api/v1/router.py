"""Agrège tous les routers de la v1 de l'API — un seul point d'inclusion dans main.py."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, users

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)

# À mesure que les modules avancent, ajouter ici : referentiel, contenu,
# assistant_ia, calendrier, paiement, espace_parent, marketplace, gamification...
