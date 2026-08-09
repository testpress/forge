from django.apps import AppConfig


class {{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
{% if cookiecutter.use_celery == 'y' %}
    def ready(self):
        # Importing for the side effect of connecting the Celery signal
        # handlers that keep BackgroundTask rows in sync.
        _ = __import__("app.domain.background_task")
{% endif %}
