"""
URL configuration for {{ cookiecutter.project_name }} project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
{% if cookiecutter.use_django_ninja == 'y' %}
from app.api.urls import api
{% endif %}
{% if cookiecutter.use_celery == 'y' %}
from app.views.ping import trigger_ping_task
{% endif %}

urlpatterns = [
    path("admin/", admin.site.urls),
{%- if cookiecutter.use_celery == 'y' %}
    path("ping-task/", trigger_ping_task, name="ping-task"),
{%- endif %}
{%- if cookiecutter.use_django_ninja == 'y' %}
    # Serves the API plus its OpenAPI schema and Swagger UI at /api/docs.
    path("api/", api.urls),
{%- endif %}
]

if settings.DEBUG:
    try:
        from debug_toolbar.toolbar import debug_toolbar_urls

        urlpatterns += debug_toolbar_urls()
    except ImportError:
        pass  # Ignore if debug_toolbar is not installed

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
