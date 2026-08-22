# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# frontend: builds the Vite/Tailwind bundle that app/helpers/vite.py's
# vite_static tag reads from frontend/dist/.vite/manifest.json. Only the
# production image needs this - dev runs the Vite dev server directly
# (see docker-compose.yml, `npm run start`), so vite_static proxies to it
# instead of reading a manifest.
# ---------------------------------------------------------------------------
FROM node:22-slim AS frontend

WORKDIR /app/frontend

# Install dependencies first, separately from the rest of frontend/, so
# this layer is only rebuilt when package.json actually changes.
COPY frontend/package.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

FROM python:3.13-slim AS base

# Install uv (see https://docs.astral.sh/uv/guide/integration/docker/)
COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /uvx /usr/local/bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies first, separately from the app code, so this layer
# is only rebuilt when pyproject.toml/uv.lock actually change.
COPY pyproject.toml uv.lock ./

# ---------------------------------------------------------------------------
# dev: used by docker-compose for local development. Includes dev
# dependencies (debug toolbar, pytest, etc.) and runs against
# config.local, with the source bind-mounted for autoreload.
# ---------------------------------------------------------------------------
FROM base AS dev

RUN uv sync --frozen --no-install-project --extra dev
COPY . .
RUN uv sync --frozen --extra dev

ENV PATH="/app/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.local

RUN chmod +x docker/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ---------------------------------------------------------------------------
# production: the default build target (`docker build .` with no --target).
# Lean image, no dev tooling, runs against config.production.
# ---------------------------------------------------------------------------
FROM base AS production

RUN uv sync --frozen --no-install-project --no-dev
COPY . .
# frontend/dist is excluded by .dockerignore (it's build output, not
# source) - pull the version built by the frontend stage instead.
COPY --from=frontend /app/frontend/dist ./frontend/dist
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.production

RUN chmod +x docker/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["docker/entrypoint.sh"]
{% if cookiecutter.use_channels == "y" -%}
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
{% elif cookiecutter.use_django_ninja == "y" -%}
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
{% else -%}
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
{% endif -%}
