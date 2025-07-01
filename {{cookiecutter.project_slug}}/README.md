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

## License

{{ cookiecutter.project_name }} is licensed under the {{ cookiecutter.open_source_license }} license.
