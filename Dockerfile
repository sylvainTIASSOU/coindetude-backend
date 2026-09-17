# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME=/opt/poetry \
    PATH="/opt/poetry/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        libpq-dev \
        gcc \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==2.4.3

WORKDIR /coindetude-backend


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
