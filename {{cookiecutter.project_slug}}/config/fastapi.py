"""
FastAPI settings configuration.
"""

import os
from typing import List


class FastAPISettings:
    """FastAPI application settings."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"
    VERSION: str = "{{ cookiecutter.version }}"
    DESCRIPTION: str = "{{ cookiecutter.description }}"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Database (for future integration with Django ORM)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # Documentation
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    RELOAD: bool = True


# Create settings instance
settings = FastAPISettings() 