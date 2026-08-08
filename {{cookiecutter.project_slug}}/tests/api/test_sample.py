from asgiref.sync import sync_to_async

from tests.base import BaseFastAPITestCase
from tests.mixins.sample import UserMixin


class TestUserAPI(BaseFastAPITestCase, UserMixin):
    async def test_user_creation(self):
        await sync_to_async(self.create_user)()
        response = await self.async_client.get("/api/v1/users/1")
        assert response.status_code == 401
