# FastAPI Integration

This directory contains the FastAPI application for {{ cookiecutter.project_name }}.

## Structure

```
app/api/
├── __init__.py           # Package initialization
├── main.py              # FastAPI app instance and configuration
├── routers/             # API route modules
│   ├── __init__.py
│   ├── auth.py          # Authentication endpoints
│   ├── users.py         # User management endpoints
│   └── health.py        # Health check endpoints
├── schemas/             # Pydantic schemas for request/response validation
│   ├── __init__.py
│   ├── auth.py          # Authentication schemas
│   ├── users.py         # User schemas
│   └── common.py        # Common response schemas
├── dependencies/        # FastAPI dependency injection
│   ├── __init__.py
│   └── auth.py          # Authentication dependencies
└── middleware/          # Custom middleware
    ├── __init__.py
    └── cors.py          # CORS configuration
```

## Getting Started

1. **Run the FastAPI server:**
   ```bash
   uv run uvicorn api:app --reload
   ```

2. **Access the API documentation:**
   - Swagger UI: http://localhost:8001/docs
   - ReDoc: http://localhost:8001/redoc

3. **Test the API:**
   ```bash
   # Health check
   curl http://localhost:8001/api/v1/health
   
   # Login
   curl -X POST http://localhost:8001/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass"}'
   ```

## Available Endpoints

### Health Checks
- `GET /api/v1/health` - Health check
- `GET /api/v1/ping` - Simple ping

### Authentication
- `POST /api/v1/auth/login` - Login to get JWT token
- `GET /api/v1/auth/me` - Get current user info (requires authentication)

### Users
- `GET /api/v1/users` - Get all users (requires authentication)
- `GET /api/v1/users/{user_id}` - Get specific user (requires authentication)
- `POST /api/v1/users` - Create new user
- `PUT /api/v1/users/{user_id}` - Update user (requires authentication)
- `DELETE /api/v1/users/{user_id}` - Delete user (requires authentication)

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login** to get an access token
2. **Include the token** in the Authorization header: `Bearer <token>`

Example:
```bash
# Login
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Use the token
curl -H "Authorization: Bearer <your-token>" \
  http://localhost:8001/api/v1/users
```

## Integration with Django

This FastAPI application is designed to work alongside your Django application:

- **Django**: Handles web interface, admin, and traditional web pages
- **FastAPI**: Handles API endpoints and modern API features

You can integrate them by:
1. Using Django models in FastAPI endpoints
2. Sharing the same database
3. Using Django's authentication system

## Development

- **Add new endpoints**: Create new files in `routers/`
- **Add new schemas**: Create new files in `schemas/`
- **Add dependencies**: Create new files in `dependencies/`
- **Run tests**: `uv run pytest tests/test_fastapi.py`

## Configuration

FastAPI settings are in `config/fastapi.py`. You can customize:
- CORS origins
- JWT settings
- Server configuration
- Documentation settings 