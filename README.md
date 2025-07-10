# Velais FastAPI Scaffold

A production-ready FastAPI project scaffold with modern Python development tools, Docker support, and comprehensive type checking. This scaffold follows Python best practices and includes everything needed to build robust, scalable APIs.

**Automatic checks on every commit:**
- ✅ **Code formatting** with Ruff
- ✅ **Type checking** with MyPy
- ✅ **Security scanning** with Bandit
- ✅ **Test execution** with pytest
- ✅ **File formatting** (trailing whitespace, end-of-file)
- ✅ **Docker linting** with Hadolint
- ✅ **OS file prevention** (prevents .DS_Store, Thumbs.db, etc.)

## ✨ Features

- 🚀 **FastAPI**: Modern, fast web framework with automatic API documentation
- 🐳 **Docker**: Multi-stage builds for development, staging, and production
- 🔧 **uv**: Ultra-fast Python package installer and resolver
- 🔍 **MyPy**: Static type checking with Pydantic v2 integration
- 🚦 **Rate Limiting**: Built-in API rate limiting with slowapi
- ⚙️ **Configuration**: Environment-based config with pydantic-settings
- 🧪 **Testing**: Comprehensive test suite with pytest
- 📝 **Documentation**: Auto-generated API docs with Swagger UI
- 🔒 **Security**: CORS middleware and production-ready configurations
- 🐛 **Debugging**: VS Code debugging support with Docker
- 📊 **Code Quality**: Pre-configured linting and formatting tools

## 🛠 Prerequisites

- **Python 3.13+** (specified in pyproject.toml)
- **uv** - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- **Docker** (optional, for containerized development)
- **Visual Studio Code** (recommended) with Python extension

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone git@github.com:Velais-Beyond-IT/velais-fastapi-scaffold.git
cd velais-fastapi-scaffold

# Install dependencies with uv
uv sync

# Activate the virtual environment
source .venv/bin/activate  # Linux/MacOS
# or
.venv\Scripts\activate     # Windows
```

### 2. Environment Configuration

Copy the example environment file and customize as needed:

```bash
cp .env.example .env
```

The `.env` file includes configuration for:
- Application environment (`ENV=development`)
- Rate limiting settings (`RATE_LIMITER=60/minute`)
- CORS configuration (automatically secure based on environment)

### 3. Run the Application

```bash
# Using uv (recommended)
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or with activated environment
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (development only)
- **Health Check**: http://localhost:8000/api/v1/health

## 🧪 Development Workflow

### Type Checking with MyPy

```bash
# Run type checking
uv run mypy src/

# Using the convenience script
./scripts/type_check.sh

# VS Code: Ctrl/Cmd+Shift+P → "Tasks: Run Task" → "mypy: Type Check"
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_health.py -v
```

### Code Quality Tools

```bash
# Type checking
uv run mypy src/

# Linting and formatting
uv run ruff check src/
uv run ruff format src/

# Security scanning
uv run bandit -r src/

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

**Setup:**
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
├── src/                         # Main application package
│   ├── __init__.py              # Package initialization with docstring
│   ├── main.py                  # FastAPI application entry point
│   │
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py          # Pydantic settings with env vars
│   │   └── limiter.py           # Rate limiting configuration
│   │
│   ├── database/                # Database models and connections
│   │   └── __init__.py          # Database package (ready for models)
│   │
│   ├── handlers/                # Custom handlers
│   │   ├── __init__.py
│   │   └── rate_limit_exceeded_handler.py
│   │
│   ├── models/                  # Data models (for database entities)
│   │   └── __init__.py
│   │
│   ├── routers/                 # API route definitions
│   │   ├── __init__.py
│   │   └── health.py            # Health check endpoint
│   │
│   ├── schemas/                 # Pydantic models for API
│   │   ├── __init__.py          # Schemas package with docstring
│   │   ├── health.py            # Health check response schema
│   │   └── limiter.py           # Rate limiting response schema
│   │
│   └── utils/                   # Utility modules
│       ├── __init__.py          # Utils package exports
│       └── cors.py              # CORS configuration utilities
│
├── tests/                       # Test suite
│   ├── test_health.py           # Health endpoint tests
│   └── test_cors.py             # CORS configuration tests
│
├── scripts/                     # Development scripts
│   ├── pre_commit_check.sh      # Pre-commit checks script
│   └── type_check.sh            # Type checking convenience script
│
├── docs/                        # Documentation
│   ├── CORS_CONFIGURATION.md    # CORS security guide
│   ├── DEVELOPMENT_GUIDE.md     # Development guidelines
│   ├── MYPY_GUIDE.md            # MyPy usage guide
│   └── SCHEMA_QUICK_REFERENCE.md # Schema development standards
│
├── .vscode/                     # VS Code configuration
│   ├── launch.json              # Debug configuration
│   ├── settings.json            # Editor settings
│   └── tasks.json               # Build/run tasks
│
├── Dockerfile.debug              # Development container with debugging
├── Dockerfile.stg                # Staging container
├── Dockerfile.prod               # Production-optimized container
├── pyproject.toml               # Project configuration with mypy settings
├── uv.lock                      # Dependency lock file
├── .env.example                 # Environment variables template
└── README.md                    # This documentation
```

## ⚙️ Configuration Management

### Environment Variables

Configure your application through environment variables in `.env`:

```env
# Application environment
ENV=development              # development, staging, production

# Rate limiting
RATE_LIMITER=60/minute       # Format: number/timeunit (second, minute, hour, day)

# CORS Configuration
CORS_ORIGINS=*               # Development: *, Production: https://yourapp.com,https://admin.yourapp.com
CORS_ALLOW_CREDENTIALS=true  # Whether to allow credentials in CORS requests
CORS_ALLOW_METHODS=*         # Allowed HTTP methods (or specific: GET,POST,PUT,DELETE,OPTIONS,PATCH)
CORS_ALLOW_HEADERS=*         # Allowed headers (or specific: Authorization,Content-Type,Accept)
CORS_MAX_AGE=86400          # Preflight cache duration in seconds

# Add your custom settings here
# DATABASE_URL=postgresql://...
# REDIS_URL=redis://...
```

### CORS Security by Environment

The application automatically adjusts CORS settings based on the environment:

| Environment | CORS Origins | Security Level |
|-------------|--------------|----------------|
| **Development** | `*` (all origins) | Permissive for fast development |
| **Staging** | Specific domains only | Secure, staging domains |
| **Production** | Specific domains only | Maximum security, HTTPS enforced |

#### Example Configurations

For local development, copy the example environment file:
```bash
cp .env.example .env
```

**Development (`.env.example`)**:
```env
ENV=development
CORS_ORIGINS=*
```

**Staging** (set via deployment):
```env
ENV=staging
CORS_ORIGINS=https://staging.yourapp.com,https://staging-admin.yourapp.com
```

**Production** (set via deployment):
```env
ENV=production
CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com,https://admin.yourapp.com
```

📖 **For comprehensive CORS security guidelines and troubleshooting, see [`docs/CORS_CONFIGURATION.md`](docs/CORS_CONFIGURATION.md)**

### Settings Class

The `src.config.settings.Settings` class manages all configuration:

```python
from src.config.settings import settings

# Access settings anywhere in your app
print(f"Environment: {settings.env}")
print(f"Rate limit: {settings.rate_limiter}")

# CORS settings
origins = settings.get_cors_origins()      # Returns list of allowed origins
methods = settings.get_cors_methods()      # Returns list of allowed methods
headers = settings.get_cors_headers()      # Returns list of allowed headers
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
RATE_LIMITER=60/minute
```

### Exempting Endpoints:
```python
from src.config.limiter import limiter

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
uv run pytest --cov=src --cov-report=html
```

## 🚀 Production Deployment

### Environment Setup:
1. Set `ENV=production` in your environment
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
- Returns: `{"status": "healthy", "timestamp": "2025-01-08T..."}`

## 📋 Schema Development Standards

This project follows domain-driven schema organization using Pydantic v2. All API schemas are organized by business domain for better maintainability and team collaboration.

### Schema Organization

```
src/schemas/
├── __init__.py              # Main exports - all schemas imported here
├── common.py               # Shared base models and utilities
├── types.py                # Custom Pydantic types and validators
├── health.py               # Health check schemas
├── limiter.py              # Rate limiting schemas
└── [domain].py             # Domain-specific schemas (users, orders, etc.)
```

### Adding New Schemas

#### 1. Choose the Right Location

**For new features/domains:**
```python
# Create: src/schemas/users.py
# Create: src/schemas/orders.py
# Create: src/schemas/products.py
```

**For shared/common patterns:**
```python
# Add to: src/schemas/common.py
# Add to: src/schemas/types.py
```

#### 2. Follow Naming Conventions

```python
# ✅ Recommended naming patterns
class UserCreateRequest(BaseModel):      # Request models
class UserResponse(BaseModel):           # Response models
class UserUpdateRequest(BaseModel):      # Update requests
class UserListResponse(BaseModel):       # List responses
class UserSearchFilters(BaseModel):      # Filter/query models

# ❌ Avoid these patterns
class User(BaseModel):                   # Too generic
class UserModel(BaseModel):              # Redundant suffix
class CreateUser(BaseModel):             # Inconsistent order
```

#### 3. Domain Schema Template

When creating a new domain file (e.g., `src/schemas/users.py`):

```python
"""User-related Pydantic schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from .common import BaseResponse, PaginatedResponse


class UserBase(BaseModel):
    """Base user model with shared fields."""
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(description="User's email address")


class UserCreateRequest(UserBase):
    """Schema for creating a new user."""
    password: str = Field(min_length=8, description="User password")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "securepassword123"
            }
        }
    }


class UserResponse(UserBase):
    """Schema for user response data."""
    id: UUID = Field(description="Unique user identifier")
    created_at: datetime = Field(description="When user was created")

    model_config = {"from_attributes": True}  # Enable ORM mode


class UserListResponse(PaginatedResponse[UserResponse]):
    """Paginated response for user lists."""
    pass
```

#### 4. Update Schema Exports

**Always add new schemas to `src/schemas/__init__.py`:**

```python
# Add your new imports
from .users import (
    UserCreateRequest,
    UserResponse,
    UserListResponse
)

# Add to __all__ list
__all__ = [
    # ... existing exports ...
    # Users
    "UserCreateRequest",
    "UserResponse",
    "UserListResponse",
]
```

#### 5. Use in Routers

```python
from fastapi import APIRouter
from src.schemas import UserCreateRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreateRequest) -> UserResponse:
    """Create a new user."""
    # Implementation here
    pass
```

### Schema Best Practices Checklist

When creating schemas, ensure you:

- [ ] **Use descriptive names** with proper suffixes (`Request`, `Response`)
- [ ] **Add docstrings** to all classes
- [ ] **Include field descriptions** using `Field(description="...")`
- [ ] **Add validation** with Field constraints (min_length, pattern, etc.)
- [ ] **Provide examples** using `model_config` with `json_schema_extra`
- [ ] **Use type hints** properly (`Optional`, `List[T]`, `Literal`)
- [ ] **Export in `__init__.py`** for easy imports
- [ ] **Follow domain organization** (group related schemas)
- [ ] **Use base models** for shared fields
- [ ] **Enable ORM mode** with `from_attributes=True` when needed

### Common Patterns

**Pagination**:
```python
from .common import PaginatedResponse

class ProductListResponse(PaginatedResponse[ProductResponse]):
    pass
```

**Base + Specific Models**:
```python
class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreateRequest(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
```

**Custom Validation**:
```python
from pydantic import field_validator

class UserCreateRequest(BaseModel):
    username: str

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
```

📖 **For detailed schema development guidelines, see `docs/DEVELOPMENT_GUIDE.md`**

## 🤝 Contributing

1. **Setup Development Environment**:
   ```bash
   uv sync
   source .venv/bin/activate
   ```

2. **Run Quality Checks**:
   ```bash
   uv run mypy src/         # Type checking
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
