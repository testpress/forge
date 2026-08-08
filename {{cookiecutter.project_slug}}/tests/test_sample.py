from app.models import Permission
from tests.base import BaseTestCase
from tests.mixins.sample import UserMixin


class TestUser(BaseTestCase, UserMixin):
    def test_create_user(self):
        user = self.create_user()

        assert user.pk is not None
        assert user.phone_number

    def test_add_and_check_permission(self):
        user = self.create_user()
        permission = Permission.objects.create(codename="view_reports", name="View reports")

        user.add_perm(permission)

        assert user.has_perm("view_reports")

    def test_superuser_has_all_permissions(self):
        user = self.create_user(is_superuser=True, is_active=True)
        Permission.objects.create(codename="view_reports", name="View reports")

        assert user.has_perm("view_reports")
