##  How to Create a New Project Using This Cookiecutter Template

This guide explains how to scaffold a new Django project using this Cookiecutter template.

---

### Prerequisites

Ensure the following tools are installed:

* Python 3.8+

* [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html)
  Install it with:

  ```bash
  pip install cookiecutter
  ```

* [Poetry](https://python-poetry.org/docs/#installation) (if using Poetry in the template):

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

---

### Create a New Project

Use the template to scaffold your project:

```bash
cookiecutter gh:<your-github-username>/<your-cookiecutter-repo>
```

Or locally (if you have the repo cloned):

```bash
cookiecutter path/to/your/template
```

You'll be prompted to enter details like:

* `project_name`: e.g., My Awesome App
* `project_slug`: (auto-generated or customizable)
* `author_name`: e.g., Hari Hara Nathan
* `email`: e.g., [hari@example.com](mailto:hari@example.com)
* `use_sentry`: y/n
* `open_source_license`: e.g., MIT, Apache 2.0, or "Not open source"

---

### What’s Generated

The template will create:

* A full Django project
* `.env` file with generated secret key
* `pyproject.toml` if Poetry is enabled
* Optional integrations (e.g., Sentry) based on input
* `README.md` for setup instructions

---

### ⚙️Setting up the New Project

1. **Navigate into your new project folder**:

   ```bash
   cd your-project-slug
   ```

2. **Apply migrations**:

   ```bash
   poetry run python manage.py migrate
   ```

3. **Run development server**:

   ```bash
   poetry run python manage.py runserver
   ```
---

### Custom Setup Hooks

* `.env` file is automatically created using a post-generation Python script.
* You can customize this script at: `hooks/post_gen_project.py`

---

### Running Tests

```bash
poetry run pytest
```

---
