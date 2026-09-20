# Depuis la racine du repo backend
poetry install           # si pas déjà fait
poetry run pytest app/tests/models/test_base.py -v
poetry run mypy app/models/
poetry run ruff check app/models/



# 1. Tests modèles
poetry run pytest app/tests/models/ -v

# 2. Qualité
poetry run mypy app/models/ app/db/
poetry run ruff check app/models/ app/db/ app/tests/models/

# 3. Génération de la migration initiale
poetry run alembic revision --autogenerate -m "initial schema"

# 4. Vérifier le fichier de migration généré (relire avant d'appliquer !)
# Il doit contenir : toutes les tables + enums + index + contraintes

# 5. Appliquer la migration
poetry run alembic upgrade head

# 6. Vérifier le schéma en base
docker compose exec db psql -U coindetude -d coindetude -c "\dt"

# 7. Seed
poetry run python -m app.db.seed.educational
poetry run python -m app.db.seed.plans

# 8. Vérifier les données
docker compose exec db psql -U coindetude -d coindetude -c "SELECT name, cycle FROM levels ORDER BY order_index;"
docker compose exec db psql -U coindetude -d coindetude -c "SELECT code, name, price_fcfa FROM plans ORDER BY order_index;"