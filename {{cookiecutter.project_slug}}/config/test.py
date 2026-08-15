from typing import Any
from typing import cast

from .base import *  # noqa: F403

# Use in-memory SQLite for faster tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

# Speed up tests by using an in-memory cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
}


# Disable migrations to speed up tests
class DisableMigrations:
    def __contains__(self, item: str) -> bool:
        return True

    def __getitem__(self, item: str) -> str:
        return "notmigrations"


# Django declares this setting as dict[str, str]. The object above is the
# conventional duck-typed stand-in - Django only ever asks it `in` and
# `[]` - so cast rather than ignore: the cast records that the shape is
# deliberate, where an ignore would only silence the symptom.
MIGRATION_MODULES = cast("dict[str, str]", DisableMigrations())

# Use MD5 hasher for faster tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable debug mode for testing
DEBUG = False
# TEMPLATES arrives through the star import above. mypy joins the value
# types of that dict literal down to `object`, so it cannot see that
# "OPTIONS" holds a dict; name the shape once and mutate through it.
template_options = cast("dict[str, Any]", TEMPLATES[0]["OPTIONS"])  # noqa: F405
template_options["debug"] = False

# Reduce logging output for tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
        },
    },
}
