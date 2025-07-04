import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.base")
app = Celery("{{ cookiecutter.project_slug }}")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["app.tasks"])
