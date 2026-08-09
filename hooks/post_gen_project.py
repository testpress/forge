import os
import random
import shutil
import string
import sys
import subprocess


def remove_path(path):
    """Remove a file or directory tree if it exists."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def remove_api_files():
    """Drop the API layer when django-ninja is disabled.

    Its imports (ninja, app.api) are unavailable in a project generated
    without the flag, so leaving these behind breaks pytest collection.
    """
    for path in ("app/api", "tests/conftest.py", "tests/api"):
        remove_path(path)


def remove_celery_files():
    """Drop the Celery layer when background tasks are disabled.

    These modules import celery and register the BackgroundTask models, so
    they cannot stay in a project generated without the flag.
    """
    for path in (
        "config/celery.py",
        "app/tasks",
        "app/views/ping.py",
        "app/domain/background_task.py",
        "app/models/background_task.py",
        "app/admin/admin.py",
    ):
        remove_path(path)


def generate_secret_key():
    """Generate a random Django secret key."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return "".join(random.choice(chars) for _ in range(50))


def create_env_file():
    """Create a default .env file with the necessary configurations."""
    project_directory = os.getcwd()
    env_file_path = os.path.join(project_directory, ".env")

    secret_key = generate_secret_key()
    env_content = f"""DEBUG=True
SECRET_KEY={secret_key}
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
{% if cookiecutter.use_sentry == 'y' %}
# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN=
{% endif %}
{% if cookiecutter.use_celery == 'y' %}
# Celery
# ------------------------------------------------------------------------------
CELERY_BROKER_URL=redis://localhost:6379/0
{% endif %}
{% if cookiecutter.use_django_ninja == 'y' %}
# API
# ------------------------------------------------------------------------------
# Bearer tokens are signed with SECRET_KEY above - there is no separate
# API signing key to configure.
API_TOKEN_MAX_AGE=86400
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
{% endif %}
"""

    with open(env_file_path, "w") as env_file:
        env_file.write(env_content)


def run_command(command):
    """Run a shell command and exit if it fails."""
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        sys.exit(result.returncode)


def run_command_best_effort(command):
    """Run a shell command without failing setup if it reports issues.

    djlint's --reformat exits non-zero whenever it changes (or can't fully
    fix) a file, even though the run itself succeeded - that's expected on
    first run, not a real error, so it must not abort project generation.
    """
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Note: '{command}' reported issues (exit {result.returncode}); "
              "continuing anyway.")


def setup_project():
    print("Creating .env file...")
    create_env_file()

    {% if cookiecutter.use_django_ninja != 'y' %}
    print("Removing API files (django-ninja not selected)...")
    remove_api_files()
    {% endif %}

    {% if cookiecutter.use_celery != 'y' %}
    print("Removing Celery files (background tasks not selected)...")
    remove_celery_files()
    {% endif %}

    print("Installing dependencies with uv...")
    run_command("uv sync --extra dev")

    # Jinja conditionals (e.g. optional Sentry/API/Channels/Celery blocks,
    # and the raw-block escaping templates need around Django template tags)
    # can leave stray blank lines or unsorted imports behind depending on
    # which options were chosen. Auto-fix and format so the project starts
    # clean regardless of which flags were selected.
    print("Formatting generated project with ruff...")
    run_command_best_effort("uv run ruff check --fix .")
    run_command_best_effort("uv run ruff format .")

    print("Formatting templates with djlint...")
    run_command_best_effort("uv run djlint . --reformat")

    print("Running makemigrations...")
    run_command("uv run python manage.py makemigrations")

    {% if cookiecutter.use_django_ninja == 'y' %}
    print("API enabled (django-ninja).")
    print("Start it with the rest of the site: uv run python manage.py runserver")
    print("Interactive docs: http://localhost:8000/api/docs")
    {% endif %}

    {% if cookiecutter.use_celery == 'y' %}
    print("Background tasks enabled (Celery + Redis).")
    print("Start a worker with: uv run celery -A config.celery worker -l info")
    {% endif %}

    print("Setup complete.")


if __name__ == "__main__":
    setup_project()
