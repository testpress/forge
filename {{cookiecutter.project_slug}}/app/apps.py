from django.apps import AppConfig


class {{ cookiecutter.project_slug.replace(' ', '')|capitalize }}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
