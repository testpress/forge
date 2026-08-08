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

{% if cookiecutter.use_fastapi == 'y' %}
5. Start the FastAPI server:
   ```bash
   uvicorn api:app --reload
   ```
   The API documentation will be available at: http://localhost:8001/docs
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
