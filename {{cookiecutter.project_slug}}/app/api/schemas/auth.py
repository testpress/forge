"""
Authentication schemas for the API.
"""

from pydantic import BaseModel


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data."""
    username: str | None = None 