from typing import Any

from app.models.user import User
from tests.factories.sample import UserFactory


class UserMixin:
    def create_user(self, **kwargs: Any) -> User:
        return UserFactory.create(**kwargs)

    def get_user(self, pk: int) -> User:
        return User.objects.get(pk=pk)
