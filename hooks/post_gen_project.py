import os
import random
import string


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
"""

    with open(env_file_path, "w") as env_file:
        env_file.write(env_content)


if __name__ == "__main__":
    create_env_file()
