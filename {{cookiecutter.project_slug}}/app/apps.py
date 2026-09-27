from django.apps import AppConfig


class {{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
{% if cookiecutter.use_celery == 'y' %}
    def ready(self) -> None:
        # Importing for the side effect of configuring the Dramatiq broker
        # (config.dramatiq calls dramatiq.set_broker(...) at import time)
        # and registering BackgroundTaskMiddleware. Needed in every
        # process that might call an actor's .send() - a view handling an
        # HTTP request, a shell session, a test - not just the worker
        # process, which already gets this by importing config.dramatiq
        # directly (`dramatiq config.dramatiq` on the CLI). Without it,
        # .send() would run against Dramatiq's own unconfigured default
        # broker instead of the one config/dramatiq.py sets up.
        _ = __import__("config.dramatiq")
{% endif %}
