# Forge - Django Project Template

A modern, well-structured Django project template that helps you quickly set up new Django projects with best practices and modern tooling.

## Features

- 🚀 Modern Django project structure
- 🧪 Pytest for testing
- 🎨 Code formatting and linting with ruff
- 📝 Template linting with djLint
- 🔍 Pre-commit hooks for code quality
- 📚 Documentation setup
- 🌍 Localization support
- 🛠️ Modular project structure
- 📦 uv for dependency management
- 🔄 Optional WebSocket support with Django Channels
- 🚀 Optional REST API with django-ninja (Pydantic schemas, OpenAPI docs)
- ⏱️ Optional background tasks with Celery + Redis
- 🐳 Docker + docker-compose for local development
- ✅ GitHub Actions CI (lint, type-check, migrations check, tests)

## Prerequisites

- Python 3.13 or higher
- [Cookiecutter](https://cookiecutter.readthedocs.io/) (`pip install cookiecutter`)
- [uv](https://docs.astral.sh/uv/) for dependency management
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose (optional, for the containerized dev setup)

## Usage

1. Create a new project using the template:

```bash
cookiecutter https://github.com/testpress/forge.git
```

2. Follow the prompts to configure your project:
   - Project name
   - Project description
   - Author name
   - Email
   - Version
   - License
   - Optional integrations:
     - Preline UI components
     - Sentry error tracking
     - Django Channels for WebSocket support
     - django-ninja for a REST API
     - Celery + Redis for background tasks (the one option that defaults
       to "y"; answer "n" to keep the project free of a Redis dependency)

3. Navigate to your new project directory:
```bash
cd your_project_name
```

4. Install dependencies using uv:
```bash
uv sync
```

5. Initialize git and install pre-commit hooks:
```bash
git init
pre-commit install
```

6. Run migrations:
```bash
uv run python manage.py migrate
```

7. Start the development server:
```bash
uv run python manage.py runserver
```

Alternatively, skip steps 4-7 and run everything (Django, Postgres, and —
if you enabled Celery or Channels — Redis and a worker) with Docker Compose
instead:

```bash
cd your_project_name
docker compose up --build
```

This serves the app at http://localhost:8000 with `config.local` settings and
autoreload; source changes on the host are reflected immediately. See
[Docker](#docker) below for details.

## Project Structure

```
your_project_name/
├── app/                    # Main application directory
│   ├── api/               # django-ninja API (if enabled)
│   │   ├── urls.py        # The NinjaAPI instance
│   │   ├── security.py    # Bearer auth over django.contrib.auth
│   │   ├── routers/       # API route modules
│   │   └── schemas/       # Pydantic schemas
│   ├── models/            # Django models
│   ├── tasks/             # Celery tasks (if enabled)
│   ├── views/             # Django views
│   └── templates/         # Django templates
├── frontend/               # Vite/Tailwind project (package.json, css/, js/)
├── config/                # Project settings and configuration
├── docker/                # Container entrypoint script
├── docs/                  # Documentation
├── locale/                # Translation files
├── tests/                 # Test suite
├── .github/workflows/     # CI (ruff, mypy, djlint, migrations, pytest)
├── manage.py             # Django management script
├── Dockerfile             # Multi-stage: frontend, dev (compose) and production targets
├── docker-compose.yml     # Local dev stack: web, Postgres (+ Redis/worker)
├── docker-compose.prod.yml # Production stack (see Production Deployment below)
├── scripts/deploy.sh      # Single-command production deploy
├── pyproject.toml        # Project dependencies and tooling config
└── uv.lock              # Locked dependencies
```

## Development

- Run tests: `uv run pytest`
- Format code: `uv run ruff format .` and `uv run ruff check --fix .`
- Lint templates: `uv run djlint .`
- Check code quality: `pre-commit run --all-files`
- Add new dependencies: `uv add package-name`
- Add development dependencies: `uv add --dev package-name`

## Docker

`docker compose up --build` starts these services:

| Service  | When | What it is |
|----------|------|------------|
| `web`    | always | Django dev server (`config.local`, `DEBUG=True`, autoreload via bind mount) on port 8000 |
| `db`     | always | Postgres 17 on port 5432 (credentials via `POSTGRES_*` env vars, default `postgres`/`postgres`) |
| `redis`  | `use_celery` or `use_channels` | Redis 7 on port 6379 |
| `worker` | `use_celery` | Celery worker, same image, no autoreload |

The image is a multi-stage `Dockerfile` with two targets:
- `dev` (what `docker-compose.yml` builds) — installs dev dependencies too
  (debug toolbar, pytest, ruff, ...) and runs `config.local`.
- `production` (the default target for a plain `docker build .`, no
  `--target` needed) — lean, no dev tooling, runs `config.production`. The
  server depends on the flags: `daphne` with Channels, `uvicorn` with
  django-ninja (its operations are async), otherwise `gunicorn`.

Both targets share an entrypoint (`docker/entrypoint.sh`) that runs
`migrate` and `collectstatic` before starting the server. The `worker`
service skips this (it just needs the `web` service to have already
migrated) so the two containers don't race to create the schema.

To build a production image standalone:
```bash
docker build -t your_project_name .
```

## Production Deployment

`docker-compose.prod.yml` is the self-hosted deploy target: the
`production` Dockerfile target (no dev tooling, no source bind mount —
the built image is the deployable artifact), Postgres with a persisted
volume, and — for whichever of Redis, Celery's worker, and Channels you
enabled — those services too, all with `restart: unless-stopped`.

1. Create a **production** `.env` (the one generated at project creation
   is for local development only — `DEBUG=True`, SQLite, a permissive
   `ALLOWED_HOSTS`). At minimum it needs:
   ```
   DEBUG=False
   SECRET_KEY=<a real, unique secret>
   ALLOWED_HOSTS=your-domain.com
   POSTGRES_PASSWORD=<a real password>
   ```
   plus `SENTRY_DSN` (required if Sentry is enabled) and
   `CORS_ALLOWED_ORIGINS` (if django-ninja is enabled). See
   `config/production.py` for the full list.
2. Deploy:
   ```bash
   ./scripts/deploy.sh
   ```
   which is exactly `docker compose -f docker-compose.prod.yml up -d --build`
   — safe to re-run for later deploys, since Compose only rebuilds and
   restarts what changed, and `docker/entrypoint.sh` runs `migrate` and
   `collectstatic` on every container start.

This starts the app on `${WEB_PORT:-8000}`; put a reverse proxy or CDN in
front of it for TLS termination. Static files are served directly by the
app via [WhiteNoise](https://whitenoise.readthedocs.io/) with
content-hashed filenames and far-future cache headers (see `STATIC_URL`
in `config/base.py`), so a CDN placed in front as a caching reverse proxy
— Cloudflare, CloudFront, etc. — can cache them at the edge without any
S3/GCS bucket in between; no separate static-asset pipeline to run.

## Continuous Integration

Every generated project ships with `.github/workflows/ci.yml`, running on
push/PR against `main` via `uv`:
- **lint**: `ruff check`, `ruff format --check`, `djlint --check`
- **typecheck**: `mypy .` (non-blocking — `continue-on-error: true` — until
  the codebase is fully annotated; see the job's comment in the workflow)
- **migrations**: `makemigrations --check --dry-run`
- **test**: `pytest --cov`

All of these run against SQLite with dummy credentials, so no services or
secrets are required for CI to pass.

## Optional Features

### Preline UI Components
If you selected "y" for `use_preline`, the template includes Preline UI components for a modern, responsive design.

### Sentry Integration
If you selected "y" for `use_sentry`, the template includes Sentry configuration for error tracking and monitoring.

### Django Channels
If you selected "y" for `use_channels`, the template includes:
- Django Channels for WebSocket support
- Redis channel layer configuration
- ASGI application setup
- Example WebSocket consumer structure

To use WebSockets:
1. Make sure Redis is running on localhost:6379
2. Add your WebSocket consumers in `app/consumers.py`
3. Configure WebSocket routing in `config/asgi.py`
4. Run the server with Daphne: `uv run daphne config.asgi:application`

### REST API (django-ninja)
If you selected "y" for `use_django_ninja`, the template includes:
- A `NinjaAPI` mounted at `/api/` in the project's own URLconf
- Bearer authentication built on `django.contrib.auth`
- User CRUD endpoints using Django's **async** ORM
- Auto-generated OpenAPI docs at `/api/docs`
- CORS via `django-cors-headers`
- Pydantic schemas, with `ModelSchema` deriving fields from Django models

There is no second server and no second port — the API is served by
`manage.py runserver` (and by `uvicorn config.asgi:application` in the
Docker image) alongside everything else:

- Interactive docs: http://localhost:8000/api/docs
- Login: `POST http://localhost:8000/api/v1/auth/login`
- Users: `GET http://localhost:8000/api/v1/users/`

See `app/api/README.md` in a generated project for the full endpoint list.

**Why django-ninja rather than FastAPI?** Earlier versions of this template
bolted a FastAPI app onto the ASGI application. That gave the API its own
JWT stack, its own signing key and its own idea of what a user is, none of
which talked to Django's session auth or ORM — and mounting it under
`config.asgi` made it mutually exclusive with Channels. django-ninja offers
the same developer experience (type hints, Pydantic, generated OpenAPI
docs) while running as ordinary Django, so authentication, middleware,
models and tests are all shared with the rest of the project.

### Background tasks (Celery + Redis)
If you selected "y" for `use_celery` (the default), the template includes:
- A configured Celery app in `config/celery.py`
- Example tasks in `app/tasks/`
- A `BackgroundTask` model recording each run's status, progress events and
  output files, plus the signal handlers that keep it up to date
- A `worker` and `redis` service in `docker-compose.yml`

Run a worker with:
```bash
uv run celery -A config.celery worker --loglevel=info
```

Answer "n" and none of the above is generated — no `celery`/`redis`
dependency, no broker to run, no Redis service in Compose.

> **Why this flag defaults to "y" when every other optional flag defaults
> to "n":** the others are additive, so "n" gives you what the template
> always gave you. Celery was unconditional before it was put behind a
> flag, so defaulting it off would change what an existing user's bake
> produces — silently dropping models and a migration from a project that
> re-runs the template expecting continuity. Defaulting to "y" keeps the
> default output unchanged and makes opting out a deliberate choice.
> (`cookiecutter.json` is strict JSON and cannot carry comments, which is
> why this note lives here.)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
