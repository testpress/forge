# Migration Guide: Poetry to uv

This guide helps you migrate existing Django projects from Poetry to uv.

## Prerequisites

1. Install uv:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Make sure you have a backup of your project before starting the migration.

## Migration Steps

### 1. Update pyproject.toml

Replace the Poetry configuration with uv-compatible format:

**Before (Poetry):**
```toml
[tool.poetry]
name = "your-project"
version = "0.1.0"
description = ""
authors = ["Your Name <your.email@example.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"
Django = "5.1.7"
# ... other dependencies

[tool.poetry.group.dev.dependencies]
pytest = "8.3.2"
# ... other dev dependencies

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**After (uv):**
```toml
[project]
name = "your-project"
version = "0.1.0"
description = ""
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "Django==5.1.7",
    # ... other dependencies
]

[project.optional-dependencies]
dev = [
    "pytest==8.3.2",
    # ... other dev dependencies
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 2. Remove Poetry Files

```bash
rm poetry.lock
rm poetry.toml  # if it exists
```

### 3. Install Dependencies with uv

```bash
uv sync
```

This will create a new `uv.lock` file with locked dependencies.

### 4. Update Commands

Replace Poetry commands with uv equivalents:

| Poetry Command | uv Command |
|----------------|------------|
| `poetry install` | `uv sync` |
| `poetry add package` | `uv add package` |
| `poetry add --group dev package` | `uv add --dev package` |
| `poetry run python manage.py migrate` | `uv run python manage.py migrate` |
| `poetry run pytest` | `uv run pytest` |
| `poetry shell` | `uv shell` |

### 5. Update CI/CD Pipelines

If you have CI/CD pipelines, update them to use uv:

**Before (GitHub Actions with Poetry):**
```yaml
- name: Install Poetry
  run: |
    curl -sSL https://install.python-poetry.org | python3 -

- name: Install dependencies
  run: poetry install

- name: Run tests
  run: poetry run pytest
```

**After (GitHub Actions with uv):**
```yaml
- name: Install uv
  run: |
    curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Install dependencies
  run: uv sync

- name: Run tests
  run: uv run pytest
```

### 6. Update Documentation

Update your project's README and documentation to reflect the new uv commands.

## Benefits of uv

- **Faster**: uv is significantly faster than Poetry for dependency resolution and installation
- **Modern**: Built with Rust, offering better performance and reliability
- **Compatible**: Works with existing Python tooling and standards
- **Simple**: Cleaner configuration format and easier to use

## Troubleshooting

### Common Issues

1. **Version conflicts**: If you encounter version conflicts, uv will show detailed error messages. You may need to update your dependency specifications.

2. **Missing dependencies**: Some packages might have different names or versions in uv. Check the error messages for suggestions.

3. **Build issues**: If you have custom build scripts, you might need to update them to work with uv's build system.

### Getting Help

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub Repository](https://github.com/astral-sh/uv)
- [uv Discord Community](https://discord.gg/astral-sh)

## Rollback

If you need to rollback to Poetry:

1. Restore your original `pyproject.toml` with Poetry configuration
2. Restore `poetry.lock` if you have it
3. Run `poetry install` to restore the Poetry environment

Remember to commit your `uv.lock` file to version control for reproducible builds! 