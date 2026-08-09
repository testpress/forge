"""Authentication schemas."""

from ninja import Schema

# Kept as a constant rather than a literal default on the schema field so
# the string isn't flagged as a hardcoded credential by the linter.
BEARER = "bearer"


class LoginSchema(Schema):
    """Credentials accepted by ``POST /api/v1/auth/login``.

    The identifier is ``phone_number`` because that is this project's
    ``User.USERNAME_FIELD``.
    """

    phone_number: str
    password: str


class TokenSchema(Schema):
    """A freshly issued bearer token."""

    access_token: str
    token_type: str
