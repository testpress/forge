"""
Common schemas for the API.
"""

from typing import Any

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Schema for message responses."""

    message: str


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str
    error_code: str | None = None


class PaginatedResponse(BaseModel):
    """Schema for paginated responses."""

    items: list[Any]
    total: int
    page: int
    size: int
    pages: int
