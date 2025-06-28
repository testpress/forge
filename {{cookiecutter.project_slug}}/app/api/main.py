"""
FastAPI application for {{ cookiecutter.project_name }}.

This module provides the main FastAPI application instance and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .routers import auth, users, health

# Create FastAPI app instance
app = FastAPI(
    title="{{ cookiecutter.project_name }} API",
    description="{{ cookiecutter.description }}",
    version="{{ cookiecutter.version }}",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


def custom_openapi():
    """Custom OpenAPI schema configuration."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="{{ cookiecutter.project_name }} API",
        version="{{ cookiecutter.version }}",
        description="{{ cookiecutter.description }}",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to {{ cookiecutter.project_name }} API",
        "docs": "/docs",
        "redoc": "/redoc",
    } 