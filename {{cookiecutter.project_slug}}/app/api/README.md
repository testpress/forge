# API

The API for {{ cookiecutter.project_name }} is built with
[django-ninja](https://django-ninja.dev/): Pydantic schemas, type-hint
based request parsing and a generated OpenAPI document, running inside
Django rather than beside it.

## Structure

```
app/api/
├── __init__.py       # Package marker
├── urls.py           # The NinjaAPI instance; included by config/urls.py
├── security.py       # Bearer tokens, signed with Django's SECRET_KEY
├── routers/
│   ├── health.py     # Unauthenticated liveness endpoints
│   ├── auth.py       # Login, current user
│   └── users.py      # User CRUD
└── schemas/
    ├── auth.py
    ├── users.py
    └── common.py
```

## Getting started

The API is part of the Django application - there is no second server to
start:

```bash
python manage.py runserver
```

- Swagger UI: http://localhost:8000/api/docs
- OpenAPI schema: http://localhost:8000/api/openapi.json

Because the operations are async, production runs over ASGI
(`uvicorn config.asgi:application`); the Dockerfile already does this.

## Endpoints

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| GET | `/api/v1/health` | - | Liveness |
| GET | `/api/v1/ping` | - | Round trip |
| POST | `/api/v1/auth/login` | - | Exchange credentials for a token |
| GET | `/api/v1/auth/me` | Bearer | The token's owner |
| GET | `/api/v1/users/` | Bearer | Paginated user list |
| POST | `/api/v1/users/` | Bearer | Create a user |
| GET | `/api/v1/users/{id}` | Bearer | Fetch a user |
| PATCH | `/api/v1/users/{id}` | Bearer | Partial update |
| DELETE | `/api/v1/users/{id}` | Bearer | Delete a user |

The API is authenticated by default (`NinjaAPI(auth=BearerAuth())`).
Endpoints that must stay public opt out with `auth=None`, so a new router
is protected unless you deliberately open it.

## Authentication

Login runs through `django.contrib.auth.aauthenticate`, so it respects
`AUTHENTICATION_BACKENDS`, the configured password hashers and the
`is_active` flag. The identifier is `phone_number`, because that is this
project's `User.USERNAME_FIELD`.

```bash
# Create a user to log in as
python manage.py createsuperuser

# Get a token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+15551234567", "password": "..."}'

# Use it
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/users/
```

Tokens are signed with `django.core.signing` using the project's
`SECRET_KEY` and contain only a user id. There is no second user store and
no second signing key: rotating `SECRET_KEY` invalidates tokens and web
sessions together, and deactivating a user revokes their API access on the
next request. `API_TOKEN_MAX_AGE` (settings) controls the lifetime.

If you would rather authenticate browser clients with the session cookie
they already have, django-ninja ships `ninja.security.django_auth` - add it
to the `auth` list in `app/api/urls.py`.

## Development

- **New endpoints**: add a module under `routers/` and mount it in `urls.py`
- **New schemas**: add a module under `schemas/`; use `ModelSchema` to
  derive fields from a Django model instead of restating them
- **Run the tests**: `uv run pytest tests/api`

Every operation is `async` and uses Django's async ORM (`afirst`,
`aexists`, `acount`, `adelete`). Keeping the whole surface async is a
deliberate rule: django-ninja's `TestAsyncClient` can then be used against
any endpoint, and nothing silently blocks the event loop.
