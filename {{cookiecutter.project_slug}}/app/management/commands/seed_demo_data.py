from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from app.models import User

DEMO_PHONE_NUMBER = "9999999999"
DEMO_PASSWORD = "demo-password"  # noqa: S105


class Command(BaseCommand):
    help = "Creates a demo superuser for local development. No-op outside DEBUG."

    def handle(self, *args: Any, **options: Any) -> None:
        if not settings.DEBUG:
            self.stdout.write("DEBUG is off - skipping demo data.")
            return

        if User.objects.filter(phone_number=DEMO_PHONE_NUMBER).exists():
            self.stdout.write("Demo user already exists.")
        else:
            User.objects.create_superuser(DEMO_PHONE_NUMBER, DEMO_PASSWORD)
            self.stdout.write("Created demo user.")

        self.stdout.write(
            self.style.SUCCESS(
                f"Log in with phone number {DEMO_PHONE_NUMBER} "
                f"and password {DEMO_PASSWORD}",
            ),
        )
