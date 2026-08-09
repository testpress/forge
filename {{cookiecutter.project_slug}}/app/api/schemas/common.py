"""Schemas shared across routers.

There is no pagination schema here on purpose - django-ninja's
``@paginate`` decorator wraps the declared ``response`` type for you.
"""

from ninja import Schema


class MessageSchema(Schema):
    """A plain human-readable message."""

    message: str


class HealthSchema(Schema):
    """Liveness response."""

    status: str
    service: str
