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
- 🐳 Docker + docker-compose for local development (Postgres, Redis, Celery worker)
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

Alternatively, skip steps 4-7 and run everything (Django, Postgres, Redis, and
a Celery worker) with Docker Compose instead:

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
│   ├── views/             # Django views
│   ├── templates/         # Django templates
│   └── static/            # Django static files
├── config/                # Project settings and configuration
├── docker/                # Container entrypoint script
├── docs/                  # Documentation
├── locale/                # Translation files
├── tests/                 # Test suite
├── .github/workflows/     # CI (ruff, mypy, djlint, migrations, pytest)
├── manage.py             # Django management script
├── Dockerfile             # Multi-stage: dev (compose) and production targets
├── docker-compose.yml     # Local dev stack: web, worker, Postgres, Redis
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

`docker compose up --build` starts four services:

| Service  | What it is |
|----------|------------|
| `web`    | Django dev server (`config.local`, `DEBUG=True`, autoreload via bind mount) on port 8000 |
| `worker` | Celery worker, same image, no autoreload |
| `db`     | Postgres 17 on port 5432 (credentials via `POSTGRES_*` env vars, default `postgres`/`postgres`) |
| `redis`  | Redis 7 on port 6379 (Celery broker) |

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
