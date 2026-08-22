#!/bin/sh
# Single-command production deploy: builds the `production` Dockerfile
# target and (re)starts the full stack detached. Safe to re-run - Compose
# only rebuilds/restarts what changed, and docker/entrypoint.sh runs
# `migrate` and `collectstatic` on every container start.
#
# Usage: ./scripts/deploy.sh
set -e

cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
    echo "No .env file found in $(pwd)." >&2
    echo "Production needs its own .env (DEBUG=False, a real SECRET_KEY," >&2
    echo "ALLOWED_HOSTS, POSTGRES_PASSWORD, ...) - the one created at" >&2
    echo "project generation time is for local development only." >&2
    exit 1
fi

docker compose -f docker-compose.prod.yml up -d --build

echo
echo "Deployed. Tail logs with:"
echo "  docker compose -f docker-compose.prod.yml logs -f web"
