"""
User management endpoints for the API.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from ..schemas.users import User, UserCreate, UserUpdate
from ..dependencies.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[User])
async def get_users(current_user: dict = Depends(get_current_user)):
    """Get all users."""
    # In a real application, you would query your Django user model
    # For now, we'll return a mock response
    return [
        {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "is_active": True,
        }
    ]


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific user by ID."""
    # In a real application, you would query your Django user model
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return {
        "id": user_id,
        "username": "testuser",
        "email": "test@example.com",
        "is_active": True,
    }


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user."""
    # In a real application, you would create a user in your Django model
    # For now, we'll return a mock response
    return {
        "id": 2,
        "username": user.username,
        "email": user.email,
        "is_active": True,
    }


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int, user_update: UserUpdate, current_user: dict = Depends(get_current_user)
):
    """Update a user."""
    # In a real application, you would update the user in your Django model
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return {
        "id": user_id,
        "username": user_update.username or "testuser",
        "email": user_update.email or "test@example.com",
        "is_active": True,
    }


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a user."""
    # In a real application, you would delete the user from your Django model
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return None 