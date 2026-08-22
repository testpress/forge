# CLAUDE.md

Guidance for Claude (or any LLM) working in this repository.

## What this repo is

`forge` (testpress/forge) is a **Cookiecutter template**, not an app.
`cookiecutter https://github.com/testpress/forge.git` bakes it into a new
Django project. Two different rule sets apply depending on which part of
the tree you're editing:

- **Repo root** (`cookiecutter.json`, `hooks/`, root `pyproject.toml`,
  `.pre-commit-config.yaml`) — plain Python, line-length 79, tooling for
  the template itself.
- **`{{cookiecutter.project_slug}}/`** — the Jinja-templated project that
  gets generated. Its own `pyproject.toml` (line-length 88, force
  single-line imports) governs everything inside it. This is where almost
  all application-standards work happens, and where the rest of this
  document is scoped.

Files under `{{cookiecutter.project_slug}}/` are Jinja templates, not
plain source: `{% if cookiecutter.use_x == "y" %}` blocks gate optional
code. Don't "fix" template syntax that looks like broken Python/TOML —
check whether it's a Jinja conditional first. Root-level hooks
deliberately skip linting/formatting this tree for that reason (see the
comment block at the top of `.pre-commit-config.yaml`); it's linted only
after baking, by `post_gen_project.py` and
`.github/workflows/validate-template.yml`, which bakes every flag
combination and runs the full gate set against each.

## Architecture (generated project)

```
app/
├── admin/        # Django admin registrations
├── api/          # django-ninja REST API (only if use_django_ninja=y)
│   ├── urls.py    # NinjaAPI instance
│   ├── security.py # Bearer auth over django.contrib.auth (no separate JWT/password lib)
│   ├── routers/    # one router module per resource
│   └── schemas/    # Pydantic request/response schemas
├── domain/       # business logic that doesn't belong to a single model/view
├── forms/        # base form class + custom fields
├── helpers/      # custom template tags ONLY — every file here auto-loads as one
├── models/       # see BaseModel below
├── tasks/        # Celery tasks (only if use_celery=y)
├── templates/    # Django templates (Jinja profile for djlint)
├── utils/        # generic, non-app-specific helper functions
└── views/        # Django views

config/           # settings (base/local/production/test), asgi/wsgi, urls, celery.py
tests/            # pytest suite; tests/factories (factory-boy), tests/mixins
```

- **`app/helpers/`** is exclusively for custom template tags — don't put
  general utility code there; that's `app/utils/`.
- **`app/models/`**: one file per model (singular filename, e.g.
  `user.py`), all inheriting from `app/models/base.py`'s `BaseModel`
  (`TimeStampedModel` + `SafeDeleteModel` with `SOFT_DELETE_CASCADE` +
  `HistoricalRecords`). Never delete rows directly or skip `BaseModel` —
  soft-delete, timestamps, and history are expected on every model.
- API layer (when enabled) is async and served via uvicorn/ASGI instead
  of the gunicorn/WSGI path the plain template uses — don't mix sync-only
  assumptions into `app/api/`.
- Optional integrations are all gated by `cookiecutter.json` flags
  (`use_preline`, `use_sentry`, `use_channels`, `use_django_ninja`,
  `use_celery`). When adding a dependency or code path tied to one of
  these, gate it the same way rather than assuming it's always present.

## Preferred libraries (already in the template — don't reach for alternatives)

- Settings: `django-environ`
- Soft delete: `django-safedelete` (`SOFT_DELETE_CASCADE`)
- Timestamps / audit history: `django-model-utils` (`TimeStampedModel`) +
  `django-simple-history`
- Forms: `django-widget-tweaks`
- Background tasks: `celery[redis]` (only when `use_celery=y`)
- Realtime: `channels` + `channels-redis` + `daphne` (only when
  `use_channels=y`)
- REST API: `django-ninja` (Pydantic schemas, OpenAPI docs) — not DRF
- Errors: `sentry-sdk` (only when `use_sentry=y`)
- Images: `pillow`; DB driver: `psycopg[binary]`
- Testing: `pytest` + `pytest-django` + `factory-boy` + `faker` +
  `pytest-mock` + `pytest-asyncio` + `pytest-xdist`
- Redis is pinned `<6.5` deliberately (kombu's supported range via
  Celery's `[redis]` extra) — don't bump it past 6.4.x without checking
  that constraint first.

## Coding standards

- **Formatting/linting**: `ruff` (see `pyproject.toml` inside
  `{{cookiecutter.project_slug}}/` for the full rule selection — a wide
  set including `S` (bandit), `B`, `PL`, `TRY`, `PERF`, `RUF`, etc., with
  `force-single-line` imports). Run `ruff format .` and
  `ruff check --fix .`; don't hand-format against the grain of the config.
- **Types**: `mypy --strict` via `django-stubs`, and it's a **blocking**
  CI job across every baked flag combination. New code must be fully
  typed — no untyped defs, no unused-ignore. Test function bodies are
  still checked but don't require a `-> None` return annotation.
- **Templates**: `djlint`, Jinja profile, 2-space indent, max line length
  119 inside the generated project (79 at repo root).
- **Security-lint** (`S` / bandit rules) is enabled — don't silence it
  casually; prefer fixing the underlying issue. `tests/**` and
  `app/api/**` have narrow, justified `per-file-ignores` — check those
  comments before adding a new blanket ignore elsewhere.
- Imports: first-party is `tests`/`scripts`/`hooks` at repo root; inside
  the generated project isort uses `force-single-line = true`.

## Review checklist

Before considering a change to `{{cookiecutter.project_slug}}/` done:

- [ ] `uv run ruff format .` / `uv run ruff check --fix .` clean
- [ ] `uv run mypy .` clean (strict mode — no new untyped code)
- [ ] `uv run djlint .` clean for any touched templates
- [ ] `uv run pytest` passes
- [ ] New models inherit `BaseModel`; migrations included
- [ ] New optional-integration code is gated by the right
      `cookiecutter.json` flag, in both `cookiecutter.json`/hooks *and*
      `pyproject.toml` dependencies
- [ ] Nothing that parses Jinja-templated files as plain
      Python/TOML/YAML was added to root `.pre-commit-config.yaml`
      (see its top-of-file comment for why)
- [ ] If the change affects the generated project, sanity-check it still
      bakes cleanly for all flag combinations
      (`.github/workflows/validate-template.yml` mirrors this)

## Notes for Claude

- Don't use this file as a scratchpad for session-local task lists or
  status updates — that's what conversation/session memory is for. Keep
  this file to durable standards, architecture, and conventions.
- When something here goes stale (a library swapped, a rule changed),
  update this file as part of the same change, not as a follow-up.
