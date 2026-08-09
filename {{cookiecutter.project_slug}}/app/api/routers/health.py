"""Health check endpoints.

Mounted with ``auth=None`` so load balancers and container health checks
can reach them without credentials.

Like every other operation in this API these are ``async``. Keeping the
whole surface async is deliberate: it is one rule to remember, and it
means ``TestAsyncClient`` works against every endpoint.
"""

from django.http import HttpRequest
from ninja import Router

from app.api.schemas.common import HealthSchema
from app.api.schemas.common import MessageSchema

router = Router(auth=None)


@router.get("/health", response=HealthSchema)
async def health_check(request: HttpRequest) -> dict[str, str]:
    """Report that the application is serving requests."""
    return {"status": "healthy", "service": "{{ cookiecutter.project_name }}"}


@router.get("/ping", response=MessageSchema)
async def ping(request: HttpRequest) -> dict[str, str]:
    """Cheapest possible round trip."""
    return {"message": "pong"}
