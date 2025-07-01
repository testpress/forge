# mypy: disable-error-code="no-untyped-def"

import pytest

class BaseTestCase:
    @pytest.fixture(autouse=True)
    def _setup(self, db) -> None:
        self.db = db
        self.setup_additional()

    def setup_additional(self) -> None:
        pass

@pytest.mark.asyncio()
class BaseFastAPITestCase:
    @pytest.fixture(autouse=True)
    def _setup(self, db, api_client, async_api_client) -> None:
        self.db = db
        self.client = api_client
        self.async_client = async_api_client
        self.setup_additional()

    def setup_additional(self) -> None:
        pass
