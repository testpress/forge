"""
Django settings for {{ cookiecutter.project_name }} project.
"""

from pathlib import Path

import environ

from .custom_template_tag_loader import get_custom_template_tags

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# Application definition

# fmt: off
LOCAL_APPS = [
    "app.apps.{{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }}Config",
]
# fmt: on

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "widget_tweaks",
    "django_extensions",
{%- if cookiecutter.use_django_ninja == "y" %}
    "corsheaders",
{%- endif %}
]

{% if cookiecutter.use_channels == "y" %}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

ASGI_APPLICATION = "config.asgi.application"
{% endif %}

INSTALLED_APPS = LOCAL_APPS + DJANGO_APPS + THIRD_PARTY_APPS

MIGRATION_MODULES = {"app": "app.db.migrations"}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Must sit directly below SecurityMiddleware, per WhiteNoise's own
    # install instructions, so it can serve static files (with far-future
    # cache headers on their hashed names - see STORAGES in
    # config/production.py) before anything else on the request path.
    "whitenoise.middleware.WhiteNoiseMiddleware",
{%- if cookiecutter.use_django_ninja == "y" %}
    # Must sit above CommonMiddleware so it can answer CORS preflight
    # requests before anything else redirects or rejects them.
    "corsheaders.middleware.CorsMiddleware",
{%- endif %}
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "config.urls"


CUSTOM_TEMPLATE_TAG_FOLDERS = ["app.helpers"]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": get_custom_template_tags(CUSTOM_TEMPLATE_TAG_FOLDERS),
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {"default": env.db()}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Defaults to the app serving its own static files (via WhiteNoise - see
# MIDDLEWARE above and STORAGES in config/production.py). To front them
# with a CDN on its own domain instead (e.g. a CloudFront/Cloudflare zone
# pulling from this app as its origin), set STATIC_URL to that domain,
# e.g. "https://cdn.example.com/static/" - no other setting has to change,
# since the static and vite_static template tags just build URLs from
# this value.
STATIC_URL = env("STATIC_URL", default="static/")
STATIC_ROOT = BASE_DIR / "staticfiles"

# The Vite/Tailwind project lives in frontend/, outside any Django app's
# own static/ folder on purpose: django.contrib.staticfiles's
# AppDirectoriesFinder auto-collects every app's static/ directory
# wholesale, and it can't tell frontend/'s raw, pre-build sources (which
# reference bare package names like "tailwindcss" that only Vite can
# resolve) from frontend/dist's actual build output. Keeping the project
# root outside app/ means only the built dist/ - listed explicitly below -
# is ever seen by collectstatic.
STATICFILES_DIRS = [
    BASE_DIR / "frontend/dist",
]

VITE_DEV_SERVER_URL = "http://localhost:5173"

VITE_MANIFEST_PATH = "frontend/dist/.vite/manifest.json"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# User model
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-user-model
AUTH_USER_MODEL = "app.User"

{% if cookiecutter.use_celery == "y" -%}
# Celery
# ------------------------------------------------------------------------------
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_TASK_TRACK_STARTED = True
{%- endif %}

{% if cookiecutter.use_django_ninja == "y" -%}
# API
# ------------------------------------------------------------------------------
# How long an issued bearer token stays valid, in seconds. Tokens are signed
# with SECRET_KEY, so rotating SECRET_KEY revokes every outstanding token.
API_TOKEN_MAX_AGE = env.int("API_TOKEN_MAX_AGE", default=60 * 60 * 24)

# Origins allowed to call the API from a browser. Override per environment;
# an empty list means same-origin requests only.
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["http://localhost:3000", "http://127.0.0.1:3000"],
)
CORS_ALLOW_CREDENTIALS = True
{%- endif %}
