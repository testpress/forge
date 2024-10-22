from typing import ClassVar

from app.models import BaseModel, Permission, Profile
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteManager


class UserManager(BaseUserManager, SafeDeleteManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and return a regular user with a phone number and password.
        """
        if not phone_number:
            message = "The Phone Number must be set"
            raise ValueError(message)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Profile.objects.create(user=user)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Create and return a superuser with a phone number and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            message = "Superuser must have is_staff=True."
            raise ValueError(message)
        if extra_fields.get("is_superuser") is not True:
            message = "Superuser must have is_superuser=True."
            raise ValueError(message)

        return self.create_user(phone_number, password, **extra_fields)


class UserPermission(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "permission",
        )

    def __str__(self):
        return f"{self.user} - {self.permission}"


class User(AbstractUser, BaseModel):
    username = None
    groups = None
    phone_number = models.CharField(max_length=15, unique=True, db_index=True)
    user_permissions = models.ManyToManyField(
        Permission,
        through=UserPermission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS: ClassVar = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def get_user_permissions(self):
        return set(self.user_permissions.values_list("codename", flat=True))

    def get_all_permissions(self, obj=None):
        if self.is_superuser and self.is_active:
            return set(Permission.objects.values_list("codename", flat=True))
        return self.get_user_permissions() | self.get_role_permissions()

    def has_perm(self, perm, obj=None):
        if self.is_superuser and self.is_active:
            return True
        return perm in self.get_all_permissions()

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm) for perm in perm_list)

    def has_module_perms(self, app_label):
        if self.is_superuser and self.is_active:
            return True
        return any(
            perm.startswith(app_label) for perm in self.get_all_permissions()
        )

    def add_perm(self, permission):
        UserPermission.objects.get_or_create(user=self, permission=permission)

    def remove_perm(self, permission):
        UserPermission.objects.filter(
            user=self,
            permission=permission,
        ).delete()
