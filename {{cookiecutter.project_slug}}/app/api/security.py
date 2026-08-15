"""Authentication for the {{ cookiecutter.project_name }} API.

There is deliberately no second user store and no second signing key here.
Tokens are signed with Django's own ``SECRET_KEY`` through
``django.core.signing`` and carry nothing but a user id, so every request
resolves back to a real ``django.contrib.auth`` user. Rotating
``SECRET_KEY`` invalidates API tokens and web sessions together, and a
deactivated user loses API access immediately.
"""

from typing import TYPE_CHECKING
from typing import Any

from django.conf import settings
from django.core import signing
from django.http import HttpRequest
from ninja.security import HttpBearer

from app.models import User

# Namespaces these signatures so a token can never be replayed against
# another use of django.core.signing elsewhere in the project.
SIGNING_SALT = "{{ cookiecutter.project_slug }}.api.auth"

if TYPE_CHECKING:
    # django-ninja assigns the authenticated principal to `request.auth`
    # but ships no typed request class to declare it on. Endpoints behind
    # BearerAuth can annotate their request with this instead, which
    # states what the auth class guarantees and keeps `request.auth`
    # checked as a User rather than an unknown attribute. At runtime it is
    # exactly HttpRequest.
    class AuthedRequest(HttpRequest):
        auth: User
else:
    AuthedRequest = HttpRequest


def create_access_token(user: User) -> str:
    """Issue a signed bearer token for ``user``."""
    return signing.dumps({"user_id": user.pk}, salt=SIGNING_SALT)


class BearerAuth(HttpBearer):
    """Resolve ``Authorization: Bearer <token>`` to a Django user.

    ``authenticate`` is async so it can use Django's async ORM without
    burning a thread; django-ninja adapts it for sync operations too, so
    both styles of endpoint can share this class.
    """

    async def authenticate(
        self,
        request: HttpRequest,
        token: str,
    ) -> User | None:
        try:
            data: dict[str, Any] = signing.loads(
                token,
                salt=SIGNING_SALT,
                max_age=settings.API_TOKEN_MAX_AGE,
            )
        except signing.BadSignature:
            return None

        return await User.objects.filter(
            pk=data["user_id"],
            is_active=True,
        ).afirst()
