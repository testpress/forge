"""Authentication endpoints.

Login goes through ``django.contrib.auth``, so it honours whatever is in
``AUTHENTICATION_BACKENDS``, the configured password hashers, and the
``is_active`` flag - the same rules the Django admin and any session-based
login already follow.
"""

from django.contrib.auth import aauthenticate
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from app.api.schemas.auth import BEARER
from app.api.schemas.auth import LoginSchema
from app.api.schemas.auth import TokenSchema
from app.api.schemas.users import UserSchema
from app.api.security import AuthedRequest
from app.api.security import create_access_token
from app.models import User

router = Router()

INVALID_CREDENTIALS = "Incorrect phone number or password"


@router.post("/login", response=TokenSchema, auth=None)
async def login(request: HttpRequest, payload: LoginSchema) -> dict[str, str]:
    """Exchange credentials for a bearer token."""
    user = await aauthenticate(
        request,
        phone_number=payload.phone_number,
        password=payload.password,
    )
    if user is None:
        raise HttpError(401, INVALID_CREDENTIALS)

    return {
        "access_token": create_access_token(user),
        "token_type": BEARER,
    }


@router.get("/me", response=UserSchema)
async def me(request: AuthedRequest) -> User:
    """Return the user the presented token belongs to.

    ``request.auth`` is set by ``BearerAuth`` and is a real ``User`` row;
    ``AuthedRequest`` is what tells the checker that.
    """
    return request.auth
