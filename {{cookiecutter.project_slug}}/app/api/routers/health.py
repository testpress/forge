"""
Health check endpoints for the API.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "{{ cookiecutter.project_name }} API"}


@router.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"message": "pong"} 