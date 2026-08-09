"""Fixtures for API tests.

django-ninja ships its own test clients, which call operations directly
without going through the URL resolver or an HTTP server - so these run at
unit-test speed while still exercising routing, schema validation and the
auth classes.
"""

import pytest
from ninja.testing import TestAsyncClient
from ninja.testing import TestClient

from app.api.urls import api


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(api)


@pytest.fixture
def async_api_client() -> TestAsyncClient:
    return TestAsyncClient(api)
