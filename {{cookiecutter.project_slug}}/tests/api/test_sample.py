from tests.base import BaseFastAPITestCase
from tests.mixins.sample import UserMixin

class TestUserAPI(BaseFastAPITestCase, UserMixin):
    async def test_user_creation(self):
        user = self.create_user()
        response = await self.async_client.get(f"/api/users/{user.id}")
        assert response.status_code == 200
