from .base import *  # noqa: F403

{% if cookiecutter.use_sentry == 'y' -%}
import logging

import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

{% endif -%}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # noqa: F405

# Static files
# ------------------------------------------------------------------------------
# Serve static files with hashed, content-based filenames and
# far-future cache headers, and gzip/brotli-compress them up front. This is
# what makes a CDN sitting in front of the app (see STATIC_URL in
# config/base.py) safe to cache aggressively: a changed file gets a new
# name instead of overwriting the cached one. Only enabled in production -
# local/dev keep Django's plain staticfiles storage so `runserver` doesn't
# need collectstatic to have been run first.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# WhiteNoise only serves a file with a 1-year, immutable Cache-Control
# header - the part that actually makes CDN edge-caching worthwhile - when
# its name matches this pattern; everything else falls back to a 60-second
# default. WhiteNoise's own default pattern only recognizes Django's own
# hash format (name.<12-hex-chars>.ext, from the manifest storage above).
# Vite hashes its own output independently, as name-<hash>.ext (see
# frontend/dist/.vite/manifest.json), so the pattern is widened to accept
# either a dot or a dash before the hash segment.
WHITENOISE_IMMUTABLE_FILE_TEST = r"^.+[.-][0-9a-zA-Z_-]{8,32}\.[^.]+$"

{% if cookiecutter.use_sentry == 'y' -%}
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",  # noqa: E501
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN")  # noqa: F405
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)  # noqa: F405

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)


integrations = [sentry_logging, DjangoIntegration(), RedisIntegration()]

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=integrations,
    environment=env("SENTRY_ENVIRONMENT", default="production"),  # noqa: F405
    traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),  # noqa: F405
)
{% endif %}
