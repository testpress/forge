# mypy: disable-error-code="no-untyped-def"

import pytest


class BaseTestCase:
    @pytest.fixture(autouse=True)
    def _setup(self, db) -> None:
        self.db = db
        self.setup_additional()

    def setup_additional(self) -> None:
        pass

{% if cookiecutter.use_django_ninja == 'y' %}
@pytest.mark.asyncio
class BaseAPITestCase:
    """Base class for API tests.

    Uses `transactional_db` rather than `db` on purpose. The API's
    operations are async, so Django runs their ORM calls on asgiref's
    shared worker thread - which has its own database connection. Data
    written inside the test's own transaction would be invisible from
    there, so the test data has to be really committed.
    """

    @pytest.fixture(autouse=True)
    def _setup(self, transactional_db, api_client, async_api_client) -> None:
        self.db = transactional_db
        self.client = api_client
        self.async_client = async_api_client
        self.setup_additional()

    def setup_additional(self) -> None:
        pass
{% endif %}
