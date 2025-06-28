"""
Tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient

{% if cookiecutter.use_fastapi == "y" %}
from app.api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert "redoc" in data


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data


def test_ping_endpoint():
    """Test the ping endpoint."""
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "pong"


def test_auth_login():
    """Test the authentication login endpoint."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_auth_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "wronguser", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_users_endpoint():
    """Test the users endpoint."""
    response = client.get("/api/v1/users")
    assert response.status_code == 401  # Requires authentication


def test_docs_endpoint():
    """Test that the docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint():
    """Test that the redoc endpoint is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200
{% else %}
# FastAPI tests are skipped when FastAPI is not enabled
pytest.skip("FastAPI not enabled", allow_module_level=True)
{% endif %} 