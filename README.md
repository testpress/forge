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
- 🚀 Optional FastAPI integration for modern APIs
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
     - FastAPI for modern API development

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
│   ├── api/               # FastAPI application (if enabled)
│   │   ├── routers/       # API route modules
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── dependencies/  # FastAPI dependencies
│   │   └── middleware/    # Custom middleware
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
├── api.py                # FastAPI entry point (if enabled)
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
  `--target` needed) — lean, no dev tooling, runs `config.production`{% if cookiecutter.use_channels == "y" %} via
  `daphne`{% elif cookiecutter.use_fastapi == "y" %} via `uvicorn`{% else %} via `gunicorn`{% endif %}.

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

### FastAPI Integration
If you selected "y" for `use_fastapi`, the template includes:
- Complete FastAPI application structure
- JWT authentication with password hashing
- User management API endpoints
- Automatic API documentation (Swagger/ReDoc)
- CORS middleware configuration
- Pydantic schemas for request/response validation

To use FastAPI:
1. Run the FastAPI server: `uv run uvicorn api:app --reload`
2. Access API documentation: http://localhost:8001/docs
3. Access ReDoc documentation: http://localhost:8001/redoc
4. Test authentication: POST http://localhost:8001/api/v1/auth/login
5. Test user endpoints: GET http://localhost:8001/api/v1/users

**FastAPI Features:**
- **Authentication**: JWT-based authentication with `/api/v1/auth/login`
- **User Management**: Full CRUD operations at `/api/v1/users`
- **Health Checks**: `/api/v1/health` and `/api/v1/ping`
- **Documentation**: Auto-generated OpenAPI documentation
- **CORS**: Configured for frontend development
- **Validation**: Pydantic schemas for all requests/responses

> **Known rough edge:** the paths above (`/api/v1/...`) are correct when
> running the FastAPI app standalone via `uvicorn api:app`. When served
> through `config.asgi:application` (i.e. the Docker image, or
> `daphne`/`uvicorn config.asgi:application` directly) with `use_channels`
> disabled, `config/asgi.py` mounts the same app under an *additional*
> `/api` prefix (`main_app.mount("/api", fastapi_app)`), so the real paths
> there are `/api/api/v1/...`. This is a pre-existing quirk in how the
> combined Django+FastAPI ASGI app is mounted, not something this CI/Docker
> work introduced or fixed — worth cleaning up separately.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
