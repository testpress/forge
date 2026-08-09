# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Development setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```
{% if cookiecutter.use_django_ninja == 'y' %}
## API

The API is built with [django-ninja](https://django-ninja.dev/) and is
served by the same process as the rest of the site - there is no second
server to start. With `runserver` up:

- Interactive docs: http://localhost:8000/api/docs
- OpenAPI schema: http://localhost:8000/api/openapi.json

Authentication uses `django.contrib.auth`, with bearer tokens signed by
Django's own `SECRET_KEY`. See `app/api/README.md` for the endpoint list
and details.
{% endif %}
## Docker

Alternatively, run everything (this app, Postgres, Redis, and a Celery
worker) with Docker Compose:

```bash
docker compose up --build
```

The app is served at http://localhost:8000 with autoreload; edits on the
host are picked up immediately. `docker compose down -v` tears it down and
drops the Postgres volume.

## Continuous Integration

`.github/workflows/ci.yml` runs ruff, djlint, mypy, a Django migrations
check, and pytest on every push/PR - see the file for details.

## License

{{ cookiecutter.project_name }} is licensed under the {{ cookiecutter.open_source_license }} license.
