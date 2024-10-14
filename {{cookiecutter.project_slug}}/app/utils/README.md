# `utils`

This directory is used for storing utility functions and helper modules that provide common functionality across the project. These functions are not tied to a specific app or model but serve as reusable tools to support the main application logic.

### Purpose

The `utils` folder contains modules for handling tasks such as:

- Data processing
- Formatting (dates, strings, etc.)
- Validation
- File handling
- Any other general-purpose functions

### Folder Structure

```
utils/
    ├── __init__.py
    ├── date.py
    ├── string.py
    └── validation.py
```

Each file should group related utility functions by functionality. For example, `date.py` could contain functions related to date formatting and parsing.

### Usage

Functions in the `utils` directory can be imported and used throughout the project. For example:

```python
from app.utils.date import format_date

formatted_date = format_date(my_date)
```

This setup encourages reusability and helps keep the codebase clean and organized by separating general-purpose logic from specific application logic.
