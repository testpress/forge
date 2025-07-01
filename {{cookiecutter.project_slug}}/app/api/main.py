"""
FastAPI application for {{ cookiecutter.project_name }}.

This module provides the main FastAPI application instance and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .routers import auth, users, health
from config.fastapi import settings
from .middleware.cors import get_cors_config

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
)

# Add CORS middleware
app.add_middleware(CORSMiddleware, **get_cors_config())

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


def custom_openapi():
    """Custom OpenAPI schema configuration."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME + " API",
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": settings.DOCS_URL,
        "redoc": settings.REDOC_URL,
    } 