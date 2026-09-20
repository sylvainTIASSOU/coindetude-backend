#!/usr/bin/env bash
# =============================================================================
# Entrypoint polyvalent : api | worker | migrate | shell
#
# Usage :
#   docker run ... image api       → uvicorn
#   docker run ... image worker    → arq
#   docker run ... image migrate   → alembic upgrade head
#   docker run ... image shell     → bash
# =============================================================================
set -euo pipefail

MODE="${1:-api}"

echo "🔧 CoinDetude backend — mode: $MODE"

case "$MODE" in
    api)
        # Gunicorn + Uvicorn workers (production)
        # En dev, uvicorn --reload direct est utilisé à la place
        exec gunicorn app.main:app \
            --worker-class uvicorn.workers.UvicornWorker \
            --workers "${WEB_CONCURRENCY:-2}" \
            --bind "0.0.0.0:${PORT:-8000}" \
            --timeout 60 \
            --graceful-timeout 30 \
            --access-logfile - \
            --error-logfile -
        ;;
    worker)
        exec arq app.workers.settings.WorkerSettings
        ;;
    migrate)
        exec alembic upgrade head
        ;;
    shell)
        exec /bin/bash
        ;;
    *)
        echo "❌ Mode inconnu : $MODE. Attendu : api | worker | migrate | shell"
        exit 1
        ;;
esac
