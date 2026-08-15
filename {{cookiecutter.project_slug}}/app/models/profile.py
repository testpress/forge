from typing import ClassVar

from django.conf import settings
from django.db import models

from app.models import BaseModel


class Profile(BaseModel):
    GENDER_CHOICES: ClassVar = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.user.phone_number} Profile"
