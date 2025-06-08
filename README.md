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

## Prerequisites

- Python 3.12 or higher
- [Cookiecutter](https://cookiecutter.readthedocs.io/) (`pip install cookiecutter`)

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
   - Optional integrations (Preline UI components, Sentry)

3. Navigate to your new project directory:
```bash
cd your_project_name
```

4. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

5. Install dependencies:
```bash
pip install -e ".[dev]"
```

6. Initialize git and install pre-commit hooks:
```bash
git init
pre-commit install
```

7. Run migrations:
```bash
python manage.py migrate
```

8. Start the development server:
```bash
python manage.py runserver
```

## Project Structure

```
your_project_name/
├── app/                    # Main application directory
├── config/                 # Project settings and configuration
├── docs/                   # Documentation
├── locale/                 # Translation files
├── tests/                  # Test suite
├── manage.py              # Django management script
└── pyproject.toml         # Project dependencies and tooling config
```

## Development

- Run tests: `pytest`
- Format code: `black .` and `isort .`
- Lint templates: `djlint .`
- Check code quality: `pre-commit run --all-files`

## Optional Features

### Preline UI Components
If you selected "y" for `use_preline`, the template includes Preline UI components for a modern, responsive design.

### Sentry Integration
If you selected "y" for `use_sentry`, the template includes Sentry configuration for error tracking and monitoring.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.