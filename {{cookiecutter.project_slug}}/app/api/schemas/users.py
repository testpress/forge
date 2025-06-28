"""
User schemas for the API.
"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema."""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class User(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool

    class Config:
        """Pydantic configuration."""
        from_attributes = True 