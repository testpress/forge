from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport
from httpx import AsyncClient

from app.api.main import app

@pytest.fixture()
def api_client() -> TestClient:
    return TestClient(app)

@pytest_asyncio.fixture
async def async_api_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
