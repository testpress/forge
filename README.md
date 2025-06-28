# Forge - Django Project Template

A modern, well-structured Django project template that helps you quickly set up new Django projects with best practices and modern tooling.

## Features

- 🚀 Modern Django project structure
- 🧪 Pytest for testing
- 🎨 Code formatting with black and isort
- 📝 Template linting with djLint
- 🔍 Pre-commit hooks for code quality
- 📚 Documentation setup
- 🌍 Localization support
- 🛠️ Modular project structure
- 📦 uv for dependency management
- 🔄 Optional WebSocket support with Django Channels
- 🚀 Optional FastAPI integration for modern APIs

## Prerequisites

- Python 3.12 or higher
- [Cookiecutter](https://cookiecutter.readthedocs.io/) (`pip install cookiecutter`)
- [uv](https://docs.astral.sh/uv/) for dependency management
- Redis (if using Django Channels)

## Usage

1. Create a new project using the template:

```bash
cookiecutter https://github.com/testpress/forge.git
```

2. Follow the prompts to configure your project:
   - Project name
   - Project description
   - Author name
   - Email
   - Version
   - License
   - Optional integrations:
     - Preline UI components
     - Sentry error tracking
     - Django Channels for WebSocket support
     - FastAPI for modern API development

3. Navigate to your new project directory:
```bash
cd your_project_name
```

4. Install dependencies using uv:
```bash
uv sync
```

5. Initialize git and install pre-commit hooks:
```bash
git init
pre-commit install
```

6. Run migrations:
```bash
uv run python manage.py migrate
```

7. Start the development server:
```bash
uv run python manage.py runserver
```

## Project Structure

```
your_project_name/
├── app/                    # Main application directory
│   ├── api/               # FastAPI application (if enabled)
│   │   ├── routers/       # API route modules
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── dependencies/  # FastAPI dependencies
│   │   └── middleware/    # Custom middleware
│   ├── models/            # Django models
│   ├── views/             # Django views
│   ├── templates/         # Django templates
│   └── static/            # Django static files
├── config/                # Project settings and configuration
├── docs/                  # Documentation
├── locale/                # Translation files
├── tests/                 # Test suite
├── manage.py             # Django management script
├── api.py                # FastAPI entry point (if enabled)
├── pyproject.toml        # Project dependencies and tooling config
└── uv.lock              # Locked dependencies
```

## Development

- Run tests: `uv run pytest`
- Format code: `uv run black .` and `uv run isort .`
- Lint templates: `uv run djlint .`
- Check code quality: `pre-commit run --all-files`
- Add new dependencies: `uv add package-name`
- Add development dependencies: `uv add --dev package-name`

## Optional Features

### Preline UI Components
If you selected "y" for `use_preline`, the template includes Preline UI components for a modern, responsive design.

### Sentry Integration
If you selected "y" for `use_sentry`, the template includes Sentry configuration for error tracking and monitoring.

### Django Channels
If you selected "y" for `use_channels`, the template includes:
- Django Channels for WebSocket support
- Redis channel layer configuration
- ASGI application setup
- Example WebSocket consumer structure

To use WebSockets:
1. Make sure Redis is running on localhost:6379
2. Add your WebSocket consumers in `app/consumers.py`
3. Configure WebSocket routing in `config/asgi.py`
4. Run the server with Daphne: `uv run daphne config.asgi:application`

### FastAPI Integration
If you selected "y" for `use_fastapi`, the template includes:
- Complete FastAPI application structure
- JWT authentication with password hashing
- User management API endpoints
- Automatic API documentation (Swagger/ReDoc)
- CORS middleware configuration
- Pydantic schemas for request/response validation

To use FastAPI:
1. Run the FastAPI server: `uv run uvicorn api:app --reload`
2. Access API documentation: http://localhost:8001/docs
3. Access ReDoc documentation: http://localhost:8001/redoc
4. Test authentication: POST http://localhost:8001/api/v1/auth/login
5. Test user endpoints: GET http://localhost:8001/api/v1/users

**FastAPI Features:**
- **Authentication**: JWT-based authentication with `/api/v1/auth/login`
- **User Management**: Full CRUD operations at `/api/v1/users`
- **Health Checks**: `/api/v1/health` and `/api/v1/ping`
- **Documentation**: Auto-generated OpenAPI documentation
- **CORS**: Configured for frontend development
- **Validation**: Pydantic schemas for all requests/responses

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.