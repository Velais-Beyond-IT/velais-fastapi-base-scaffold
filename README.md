# Velais FastAPI Scaffold

A production-ready FastAPI project scaffold with modern Python development tools, Docker support, and comprehensive type checking. This scaffold follows Python best practices and includes everything needed to build robust, scalable APIs.

## ✨ Features

- 🚀 **FastAPI**: Modern, fast web framework with automatic API documentation
- 🐳 **Docker**: Multi-stage builds for development, staging, and production
- 🔧 **uv**: Ultra-fast Python package installer and resolver
- � **MyPy**: Static type checking with Pydantic v2 integration
- 🚦 **Rate Limiting**: Built-in API rate limiting with slowapi
- ⚙️ **Configuration**: Environment-based config with pydantic-settings
- 🧪 **Testing**: Comprehensive test suite with pytest
- 📝 **Documentation**: Auto-generated API docs with Swagger UI
- 🔒 **Security**: CORS middleware and production-ready configurations
- � **Debugging**: VS Code debugging support with Docker
- 📊 **Code Quality**: Pre-configured linting and formatting tools

## 🛠 Prerequisites

- **Python 3.13+** (specified in pyproject.toml)
- **uv** - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- **Docker** (optional, for containerized development)
- **Visual Studio Code** (recommended) with Python extension

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd velais-fastapi-scaffold

# Install dependencies with uv
uv sync

# Activate the virtual environment
source .venv/bin/activate  # Linux/MacOS
# or
.venv\Scripts\activate     # Windows
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
env=development
rate_limiter=5/minute
```

### 3. Run the Application

```bash
# Using uv (recommended)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or with activated environment
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (development only)
- **Health Check**: http://localhost:8000/api/v1/health

## 🧪 Development Workflow

### Type Checking with MyPy

```bash
# Run type checking
uv run mypy app/

# Using the convenience script
./scripts/type_check.sh

# VS Code: Ctrl/Cmd+Shift+P → "Tasks: Run Task" → "mypy: Type Check"
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test file
uv run pytest tests/test_health_check.py -v
```

### Code Quality Tools

```bash
# Type checking
uv run mypy app/

# Linting and formatting
uv run ruff check app/
uv run ruff format app/

# Security scanning
uv run bandit -r app/

# Run tests
uv run pytest

# Pre-commit checks (all tools)
uv run pre-commit run --all-files

# Using convenience script
./scripts/pre_commit_check.sh all
```

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality before commits:

**Automatic checks on every commit:**
- ✅ **Code formatting** with Ruff
- ✅ **Type checking** with MyPy
- ✅ **Security scanning** with Bandit
- ✅ **Test execution** with pytest
- ✅ **File formatting** (trailing whitespace, end-of-file)
- ✅ **Docker linting** with Hadolint

**Setup (already done):**
```bash
uv run pre-commit install
```

**Manual execution:**
```bash
# Run on all files
uv run pre-commit run --all-files

# Run on staged files only
uv run pre-commit run

# Using convenience script
./scripts/pre_commit_check.sh
```

## 🐳 Docker Development

### Development Container

```bash
# Build development image
docker build -f Dockerfile.debug -t velais-fastapi:dev .

# Run with debugging support
docker run -p 8000:8000 -p 5678:5678 velais-fastapi:dev
```

### VS Code Debugging

1. Open project in VS Code
2. Set breakpoints in your code
3. Press F5 or use the Run and Debug panel
4. The debugger will attach to the running container

### Production Containers

```bash
# Staging build
docker build -f Dockerfile.stg -t velais-fastapi:staging .
docker run -p 8000:8000 velais-fastapi:staging

# Production build
docker build -f Dockerfile.prod -t velais-fastapi:prod .
docker run -p 8000:8000 velais-fastapi:prod
```

### Docker Features

- **🚀 uv Integration**: Ultra-fast dependency resolution and installation
- **📦 Multi-stage Builds**: Optimized for production with smaller final images
- **🔒 Security**: Non-root user and minimal attack surface
- **🏥 Health Checks**: Built-in health monitoring for production
- **🐛 Debug Support**: Remote debugging with debugpy integration

## 📁 Project Structure

```
├── app/                           # Main application package
│   ├── __init__.py               # Package initialization with docstring
│   ├── main.py                   # FastAPI application entry point
│   │
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py          # Pydantic settings with env vars
│   │   └── limiter.py           # Rate limiting configuration
│   │
│   ├── database/                # Database models and connections
│   │   └── __init__.py          # Database package (ready for models)
│   │
│   ├── handlers/                # Custom exception handlers
│   │   ├── __init__.py
│   │   └── rate_limit_exceeded_handler.py
│   │
│   ├── models/                  # Data models (for database entities)
│   │   └── __init__.py
│   │
│   ├── routers/                 # API route definitions
│   │   ├── __init__.py
│   │   └── health_check.py      # Health check endpoint
│   │
│   └── schemas/                 # Pydantic models for API
│       ├── __init__.py          # Schemas package with docstring
│       ├── health_response.py   # Health check response schema
│       └── rate_limit_exceeded_response.py
│
├── tests/                       # Test suite
│   └── test_health_check.py    # Health endpoint tests
│
├── scripts/                     # Development scripts
│   └── type_check.sh           # Type checking convenience script
│
├── docs/                        # Documentation
│   └── MYPY_GUIDE.md           # MyPy usage guide
│
├── .vscode/                     # VS Code configuration
│   ├── launch.json             # Debug configuration
│   ├── settings.json           # Editor settings
│   └── tasks.json              # Build/run tasks
│
├── Dockerfile.debug             # Development container with debugging
├── Dockerfile.stg              # Staging container
├── Dockerfile.prod             # Production-optimized container
├── pyproject.toml              # Project configuration with mypy settings
├── uv.lock                     # Dependency lock file
├── .env                        # Environment variables (create this)
└── README.md                   # This documentation
```

## ⚙️ Configuration Management

### Environment Variables

Configure your application through environment variables in `.env`:

```env
# Application environment
env=development              # development, staging, production

# Rate limiting
rate_limiter=5/minute       # Format: number/timeunit (second, minute, hour, day)

# Add your custom settings here
# DATABASE_URL=postgresql://...
# REDIS_URL=redis://...
```

### Settings Class

The `app.config.settings.Settings` class manages all configuration:

```python
from app.config.settings import settings

# Access settings anywhere in your app
print(f"Environment: {settings.env}")
print(f"Rate limit: {settings.rate_limiter}")
```

## 🔍 Type Checking

This project uses MyPy for static type checking with the following configuration:

### MyPy Configuration Features:
- **Strict mode** enabled for maximum type safety
- **Pydantic v2 plugin** for better model validation
- **Custom overrides** for third-party libraries
- **Error codes** displayed for easy troubleshooting

### Best Practices:
- All functions have type annotations
- Pydantic models use `Field()` with descriptions
- Return types are explicitly declared
- Optional types are properly handled

See `docs/MYPY_GUIDE.md` for detailed type checking guidelines.

## 🚦 Rate Limiting

Built-in rate limiting using slowapi:

### Configuration:
```python
# In .env file
rate_limiter=10/minute
```

### Exempting Endpoints:
```python
from app.config.limiter import limiter

@router.get("/unlimited")
@limiter.exempt  # type: ignore[misc]
async def unlimited_endpoint():
    return {"message": "No rate limit applied"}
```

## 🧪 Testing

### Test Structure:
- Unit tests for all endpoints
- Integration tests for database operations (when added)
- Proper test fixtures and mocking

### Running Tests:
```bash
# Run all tests
uv run pytest

# With verbose output
uv run pytest -v

# With coverage report
uv run pytest --cov=app --cov-report=html
```

## 🚀 Production Deployment

### Environment Setup:
1. Set `env=production` in your environment
2. Configure production database URLs
3. Set up proper secrets management
4. Use production Dockerfile

### Docker Production:
```bash
# Build production image
docker build -f Dockerfile.prod -t velais-fastapi:prod .

# Run production container
docker run -p 8000:8000 \
  -e env=production \
  -e rate_limiter=100/minute \
  velais-fastapi:prod
```

### Security Features:
- Swagger UI disabled in production
- CORS properly configured
- Rate limiting enabled by default
- Environment-based configuration

## 🛠 Development Tools

### VS Code Integration:
- **Tasks**: Pre-configured build and test tasks
- **Debugging**: Full Docker debugging support
- **Problem Matchers**: MyPy error highlighting
- **Extensions**: Recommended Python development extensions

### Available Tasks (Ctrl/Cmd+Shift+P → "Tasks: Run Task"):
- `mypy: Type Check` - Run static type checking
- `pre-commit: Run All Checks` - Run all quality checks
- `docker-build` - Build development container
- `docker-run: debug` - Run container with debugging

### Scripts:
- `./scripts/type_check.sh` - Convenience script for type checking
- `./scripts/pre_commit_check.sh` - Run all pre-commit checks manually

## 📚 API Documentation

### Swagger UI (Development Only):
- **URL**: http://localhost:8000/docs
- **Features**: Interactive API testing, schema visualization
- **Security**: Automatically disabled in production

### API Endpoints:
- `GET /api/v1/health` - Health check endpoint
- Returns: `{"status": "Healthy", "timestamp": "2025-01-08T..."}`

## 🤝 Contributing

1. **Setup Development Environment**:
   ```bash
   uv sync
   source .venv/bin/activate
   ```

2. **Run Quality Checks**:
   ```bash
   uv run mypy app/          # Type checking
   uv run pytest            # Tests
   ```

3. **Follow Conventions**:
   - Use type hints everywhere
   - Follow PEP 8 naming conventions
   - Add docstrings to all public functions
   - Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Troubleshooting

### Common Issues:

**uv not found**:
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Import errors in MyPy**:
- Check `pyproject.toml` for missing type stubs
- Add overrides for untyped libraries

**Docker debugging not working**:
- Ensure port 5678 is available
- Check VS Code launch configuration

**Rate limiting too strict**:
- Adjust `rate_limiter` in `.env` file
- Use `@limiter.exempt` for specific endpoints

For more help, check the documentation in the `docs/` directory.
