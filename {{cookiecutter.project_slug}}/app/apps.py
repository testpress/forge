from django.apps import AppConfig


class {{ cookiecutter.project_slug.replace(' ', '')|capitalize }}Config(AppConfig):  # noqa: E999
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        _ = __import__("app.domain.background_task")
