# `models`

This directory contains all the **Django models** that define the structure of the database for this project. Models serve as the single, definitive source of information about the data, defining both the fields and the behaviors of the data.

### Purpose

Each model in this directory represents a database table and is responsible for:

- Defining the fields and relationships for your data.
- Providing an API for querying and managing records.
- Handling validation, constraints, and other database-related operations.

### Folder Structure

```
models/
    ├── __init__.py
    ├── base.py
    ├── user.py
    ├── product.py
    └── order.py
```

### File Naming Convention

- **Singular File Names**: Use **singular** names for model files (e.g., `user.py`, `product.py`). Each file represents a single entity or a group of closely related entities. This follows the convention of naming Django models (classes) in singular form (e.g., `User`, `Product`).

### BaseModel

All models in this project should inherit from the `BaseModel` class located in `app/models/base.py`. This ensures that every model has consistent behavior, such as timestamps, soft deletion, and historical tracking.

### Example Model

All models should inherit from `BaseModel`. Here’s an example of a basic model:

```python
from django.db import models
from app.models.base import BaseModel

class User(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
```

### Best Practices

- **Separation of concerns**: Group related models together in a single file when appropriate, but avoid overly large files.
- **Naming conventions**: Use singular nouns for both model names and file names (`User`, `Product`).
- **Relationships**: Leverage Django’s powerful relationships (ForeignKey, OneToOneField, ManyToManyField) to define how models interact with each other.

### Managing Models

- **Migrations**: Ensure you create and apply migrations after modifying or adding new models.
- **Querying**: Use Django’s ORM to query models and interact with the database. Example:
  
```python
from app.models.user import User

users = User.objects.all()
```

This setup ensures consistent behavior across all models while maintaining a clean and organized structure.
