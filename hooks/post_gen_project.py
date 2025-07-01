import os
import random
import string
import sys
import subprocess

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
{% if cookiecutter.use_fastapi == 'y' %}
# FastAPI
# ------------------------------------------------------------------------------
FASTAPI_SECRET_KEY={secret_key}
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8001
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


def setup_project():
    print("Creating .env file...")
    create_env_file()

    print("Installing dependencies with uv...")
    run_command("uv sync --extra dev")

    print("Running makemigrations...")
    run_command("uv run python manage.py makemigrations")

    {% if cookiecutter.use_fastapi == 'y' %}
    print("FastAPI integration enabled!")
    print("To run the FastAPI server: uv run uvicorn api:app --reload")
    print("API documentation will be available at: http://localhost:8001/docs")
    {% endif %}

    print("Setup complete.")


if __name__ == "__main__":
    setup_project()
