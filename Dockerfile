# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

# --- Métadonnées ---
LABEL org.opencontainers.image.title="CoinDetude Backend"
LABEL org.opencontainers.image.description="API FastAPI pour la plateforme CoinDetude"

# --- Variables d'environnement ---
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/opt/poetry/bin:$PATH"

# --- Dépendances système ---
# - build-essential : compilation de paquets natifs (asyncpg, hiredis...)
# - libpq-dev       : client PostgreSQL (utile pour psql en debug)
# - curl            : healthchecks
# - git             : Poetry peut vouloir cloner des deps git
# - make            : utile pour les Makefile éventuels
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libpq-dev \
        postgresql-client \
        make \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==2.4.3

WORKDIR /coindetude-backend

# --- Santé par défaut (utile pour le devcontainer) ---
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:8000/api/v1/health || exit 1

# ---------- Développement (utilisé par .devcontainer) ----------
FROM base AS development

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --with dev

COPY . .
RUN poetry install --with dev

EXPOSE 8000
CMD ["poetry", "run", "fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]


# ---------- Production ----------
FROM base AS production

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --only main

COPY app ./app
RUN poetry install --only main

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
CMD ["poetry", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
