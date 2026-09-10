# CoinDétude — API Backend

API FastAPI de CoinDétude, plateforme de révision pour les élèves togolais
(CEPD, BEPC, BAC).

## Stack

- **FastAPI** (async) + **Pydantic v2**
- **SQLAlchemy 2.0** (style `Mapped`/`mapped_column`, async) + **asyncpg**
- **Alembic** pour les migrations
- **Poetry** pour la gestion des dépendances
- **Argon2** (hash mots de passe) + **PyJWT** (tokens)
- **Cloudflare R2** (stockage fichiers, compatible S3) via boto3
- **Firebase Admin SDK** (notifications push FCM)
- **Ruff** (lint + format) et **mypy** (typage strict)

## Démarrage rapide (devcontainer — recommandé)

1. Ouvrir le dossier dans VS Code avec l'extension **Dev Containers** installée.
2. `Ctrl+Shift+P` → **Dev Containers: Reopen in Container**.
3. VS Code construit l'image, lance Postgres + Adminer, installe les
   dépendances Poetry et les hooks pre-commit automatiquement
   (`postCreateCommand`).
4. Copier `.env.example` vers `.env` et renseigner au minimum `SECRET_KEY` :
   ```bash
   cp .env.example .env
   python -c "import secrets; print(secrets.token_urlsafe(64))"
   ```
5. Appliquer les migrations puis lancer le serveur :
   ```bash
   make migrate
   make dev
   ```
6. API sur http://localhost:8000/docs — Adminer sur http://localhost:8080
   (système `PostgreSQL`, serveur `db`, utilisateur/mdp/base comme dans `.env`).

## Démarrage sans devcontainer

```bash
docker compose up -d db adminer
poetry install --with dev
cp .env.example .env  # puis éditer, en gardant POSTGRES_SERVER=localhost
poetry run alembic upgrade head
poetry run fastapi dev app/main.py
```

## Commandes utiles

| Commande            | Effet                                              |
|---------------------|-----------------------------------------------------|
| `make dev`           | Lance le serveur avec rechargement à chaud          |
| `make test`          | Lance la suite de tests avec couverture             |
| `make lint`          | Ruff + mypy                                         |
| `make format`        | Formatte et corrige automatiquement                 |
| `make revision m="…"`| Génère une migration Alembic à partir des modèles   |
| `make migrate`       | Applique les migrations en attente                  |

## Structure

```
app/
  core/        # config, sécurité (JWT/argon2), logging
  db/          # base déclarative SQLAlchemy + session async
  models/      # modèles SQLAlchemy 2.0 (un fichier par domaine)
  schemas/     # schémas Pydantic (entrée/sortie API)
  api/
    deps.py    # dépendances communes (DB, utilisateur courant)
    v1/
      router.py       # agrège tous les routers
      endpoints/       # un fichier par ressource
  services/    # intégrations externes (R2, FCM, PayGate...)
  tests/       # tests pytest (async, DB isolée par test)
alembic/       # migrations
```

## Prochaines étapes

- Porter le schéma des 26 tables déjà validé (référentiel pédagogique,
  contenu, IA assistant, calendrier/actualités, paiement, espace parent,
  marketplace enseignants, gamification, administration) dans `app/models/`,
  un module par domaine.
- Ajouter les routers correspondants sous `app/api/v1/endpoints/`.
- Brancher le pipeline de scraping/OCR (Tesseract) comme job séparé
  (script ou worker), pas dans le cycle requête/réponse de l'API.
- Intégrer PayGate Global (webhook de confirmation de paiement mobile money)
  et FCM pour les notifications.
