"""
Common schemas for the API.
"""

from pydantic import BaseModel
from typing import Any, Optional


class MessageResponse(BaseModel):
    """Schema for message responses."""
    message: str


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None


class PaginatedResponse(BaseModel):
    """Schema for paginated responses."""
    items: list[Any]
    total: int
    page: int
    size: int
    pages: int 