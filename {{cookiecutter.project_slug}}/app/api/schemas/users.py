"""User schemas.

``UserSchema`` is a ``ModelSchema``: its fields are derived from the Django
model, so a model change shows up in the API and in the generated OpenAPI
document without a second declaration to keep in sync.
"""

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from ninja import ModelSchema
from ninja import Schema
from pydantic import field_validator

from app.models import User


class EmailValidationMixin(Schema):
    """Validate an optional ``email`` field with Django's own validator.

    ``check_fields=False`` is required because this mixin does not declare
    ``email`` itself - the schemas that inherit it do.
    """

    @field_validator("email", check_fields=False)
    @classmethod
    def validate_optional_email(cls, value: str | None) -> str | None:
        if not value:
            return value
        try:
            validate_email(value)
        except DjangoValidationError as exc:
            message = "Enter a valid email address."
            raise ValueError(message) from exc
        return value


class UserSchema(ModelSchema):
    """User representation returned by the API."""

    class Meta:
        model = User
        fields = ("id", "phone_number", "email", "is_active")


class UserCreateSchema(EmailValidationMixin):
    """Payload for creating a user."""

    phone_number: str
    password: str
    email: str = ""


class UserUpdateSchema(EmailValidationMixin):
    """Payload for a partial update. Omitted fields are left untouched."""

    phone_number: str | None = None
    email: str | None = None
    is_active: bool | None = None
