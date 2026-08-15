from collections.abc import Iterable
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar

from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.managers import SafeDeleteManager

from app.models import BaseModel
from app.models import Permission
from app.models import Profile

if TYPE_CHECKING:
    from django.db.models import Model


class UserManager(BaseUserManager["User"], SafeDeleteManager):
    def create_user(
        self,
        phone_number: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "User":
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

    def create_superuser(
        self,
        phone_number: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "User":
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

    # Async counterparts, mirroring django.contrib.auth.models.UserManager.
    # Django only generates these for its own manager, so a custom manager
    # has to provide them for async callers (e.g. the API layer).
    async def acreate_user(
        self,
        phone_number: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "User":
        return await sync_to_async(self.create_user)(
            phone_number,
            password,
            **extra_fields,
        )

    async def acreate_superuser(
        self,
        phone_number: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "User":
        return await sync_to_async(self.create_superuser)(
            phone_number,
            password,
            **extra_fields,
        )


class UserPermission(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "permission",
        )

    def __str__(self) -> str:
        return f"{self.user} - {self.permission}"


class User(AbstractUser, BaseModel):
    # Setting an inherited field to None is Django's documented way to drop
    # it. The base classes declare real field types and the type system has
    # no way to express a removal, so these read as incompatible overrides.
    # Ignored deliberately and narrowly; the alternative is not inheriting
    # from AbstractUser at all.
    username = None  # type: ignore[assignment]
    groups = None  # type: ignore[assignment]
    phone_number = models.CharField(max_length=15, unique=True, db_index=True)
    # Likewise: this points at the project's own Permission model, while
    # PermissionsMixin declares django.contrib.auth's. That substitution is
    # the entire purpose of the field.
    user_permissions = models.ManyToManyField(  # type: ignore[assignment]
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

    # AbstractUser declares `objects` as django.contrib.auth's UserManager.
    # This project's manager is built on BaseUserManager instead, because
    # create_user takes a phone number rather than a username, so the two
    # cannot line up. ClassVar is what stops it additionally being reported
    # as an instance variable shadowing a class variable.
    objects: ClassVar[UserManager] = UserManager()  # type: ignore[assignment]

    def __str__(self) -> str:
        return self.phone_number

    # The `obj` parameters below go unused here, but the signatures have to
    # match PermissionsMixin: narrowing an inherited signature is unsound,
    # and mypy rejects it.
    def get_user_permissions(self, obj: "Model | None" = None) -> set[str]:
        return set(self.user_permissions.values_list("codename", flat=True))

    def get_all_permissions(self, obj: "Model | None" = None) -> set[str]:
        if self.is_superuser and self.is_active:
            return set(Permission.objects.values_list("codename", flat=True))
        return self.get_user_permissions()

    def has_perm(self, perm: str, obj: "Model | None" = None) -> bool:
        if self.is_superuser and self.is_active:
            return True
        return perm in self.get_all_permissions()

    def has_perms(
        self,
        perm_list: Iterable[str],
        obj: "Model | None" = None,
    ) -> bool:
        return all(self.has_perm(perm) for perm in perm_list)

    def has_module_perms(self, app_label: str) -> bool:
        if self.is_superuser and self.is_active:
            return True
        return any(perm.startswith(app_label) for perm in self.get_all_permissions())

    def add_perm(self, permission: Permission) -> None:
        UserPermission.objects.get_or_create(user=self, permission=permission)

    def remove_perm(self, permission: Permission) -> None:
        UserPermission.objects.filter(
            user=self,
            permission=permission,
        ).delete()
