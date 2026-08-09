"""The {{ cookiecutter.project_name }} API.

This is an ordinary Django URLconf entry, included by ``config/urls.py``.
Requests reach it through the project's normal middleware stack, so
sessions, locale, security headers, ``simple_history``'s request user and
anything else in ``MIDDLEWARE`` apply to API calls exactly as they do to
the rest of the site.
"""

from ninja import NinjaAPI

from app.api.routers import auth
from app.api.routers import health
from app.api.routers import users
from app.api.security import BearerAuth

api = NinjaAPI(
    title="{{ cookiecutter.project_name }} API",
    version="{{ cookiecutter.version }}",
    description="{{ cookiecutter.description }}",
    # Authenticated by default; endpoints that must stay public opt out
    # explicitly with `auth=None`. Failing closed is the safer default -
    # a new router is protected unless someone deliberately opens it.
    auth=BearerAuth(),
)

api.add_router("/v1", health.router, tags=["health"])
api.add_router("/v1/auth", auth.router, tags=["authentication"])
api.add_router("/v1/users", users.router, tags=["users"])
