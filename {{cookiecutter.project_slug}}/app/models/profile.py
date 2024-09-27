from typing import ClassVar

from app.models import BaseModel
from django.conf import settings
from django.db import models


class Profile(BaseModel):
    GENDER_CHOICES: ClassVar = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.phone_number} Profile"
