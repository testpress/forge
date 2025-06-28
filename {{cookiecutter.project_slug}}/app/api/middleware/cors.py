"""
CORS middleware configuration for the API.
"""

from fastapi.middleware.cors import CORSMiddleware


def get_cors_middleware():
    """Get CORS middleware configuration."""
    return CORSMiddleware(
        allow_origins=[
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://localhost:3000",  # For React/Vue frontend
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 