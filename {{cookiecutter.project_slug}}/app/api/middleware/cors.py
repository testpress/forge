"""
CORS middleware configuration for the API.
"""

def get_cors_config():
    """Return CORS middleware configuration as dict."""
    return {
        "allow_origins": [
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://localhost:3000",  # For React/Vue frontend
            "http://127.0.0.1:3000",
        ],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
