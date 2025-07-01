from app.models.user import User
from tests.factories.sample import UserFactory

class UserMixin:
    def create_user(self, **kwargs) -> User:
        return UserFactory(**kwargs)
