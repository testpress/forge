"""
ASGI config for {{ cookiecutter.project_name }} project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.local")

{% if cookiecutter.use_channels == "y" %}
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Add your WebSocket URL patterns here
    # "websocket": AuthMiddlewareStack(
    #     URLRouter([
    #         # path("ws/some_path/", YourConsumer.as_asgi()),
    #     ])
    # ),
})
{% else %}
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

django_app = get_asgi_application()
from django.conf import settings
from app.api.main import app as fastapi_app

main_app = FastAPI()
main_app.mount(
    "/static",
    StaticFiles(directory=str(settings.BASE_DIR / "app" / "static")),
    name="static",
)
main_app.mount("/api", fastapi_app)
main_app.mount("/", django_app)

application = main_app
{% endif %}
