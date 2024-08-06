# ruff: noqa: E501
from .base import *  # noqa: F403

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
