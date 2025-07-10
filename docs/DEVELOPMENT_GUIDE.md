# Development Guide

## Code Quality Tools

### Ruff: Modern Python Linting & Formatting

This project uses **Ruff** as the primary tool for linting and formatting Python code. Ruff is a modern, extremely fast replacement for multiple traditional tools.

#### Why Ruff Over Legacy Tools?

| Aspect | Legacy Tools (Pylint + Black + isort + flake8) | Ruff |
|--------|-----------------------------------------------|------|
| **Speed** | ~30-60 seconds | ~0.1-1 seconds (10-100x faster) |
| **Setup** | Multiple tools, complex configuration | Single tool, simple config |
| **Maintenance** | Multiple dependencies, version conflicts | One dependency |
| **Features** | Need multiple tools for linting + formatting | All-in-one solution |
| **Modern Python** | Some tools lag behind latest Python features | Built for modern Python (3.13+) |

#### What Ruff Replaces

- **Pylint**: Static analysis and linting → `ruff check`
- **Black**: Code formatting → `ruff format`
- **isort**: Import sorting → `ruff check --fix` (I001-I005 rules)
- **flake8**: Style guide enforcement → `ruff check`
- **pyupgrade**: Syntax modernization → `ruff check --fix` (UP rules)

#### Ruff Configuration

Our Ruff setup in `pyproject.toml`:
```toml
[tool.ruff]
target-version = "py313"      # Target Python 3.13+
line-length = 88              # Standard line length
fix = true                    # Auto-fix issues when possible

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort (import sorting)
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade (modernize syntax)
    "ARG",  # flake8-unused-arguments
    "SIM",  # flake8-simplify
]
```

#### VS Code Integration

The project is configured to use Ruff automatically in VS Code:
```json
"[python]": {
  "editor.defaultFormatter": "charliermarsh.ruff",
  "editor.codeActionsOnSave": {
    "source.fixAll.ruff": "explicit",
    "source.organizeImports.ruff": "explicit"
  }
}
```

This means:
- Code formats automatically on save
- Imports are organized automatically
- Linting errors show in real-time
- Many issues are auto-fixed

#### Manual Usage
```bash
# Check for linting issues
uv run ruff check

# Auto-fix issues
uv run ruff check --fix

# Format code
uv run ruff format

# Check if code is already formatted
uv run ruff format --check
```

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality and consistency. The hooks run automatically before each commit.

### What Gets Checked

#### Code Quality
- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Bandit**: Security vulnerability scanning

#### File Quality
- **Trailing whitespace**: Automatically removed
- **End of file**: Ensures files end with newline
- **Large files**: Prevents committing files >1MB
- **Merge conflicts**: Detects conflict markers

#### Configuration Files
- **TOML**: Validates pyproject.toml syntax
- **YAML**: Validates .yml/.yaml files
- **Dockerfiles**: Lints with Hadolint

#### Tests
- **pytest**: Runs the complete test suite

### Installation

Pre-commit is already configured! If you need to reinstall:

```bash
uv run pre-commit install
```

### Usage

#### Automatic (Recommended)
Hooks run automatically on `git commit`. If any check fails:
1. Review the output
2. Fix any issues or stage auto-fixed files
3. Commit again

#### Manual Execution
```bash
# Run on all files
uv run pre-commit run --all-files

# Run on staged files only
uv run pre-commit run

# Run specific hook
uv run pre-commit run mypy
uv run pre-commit run ruff

# Using convenience script
./scripts/pre_commit_check.sh all    # all files
./scripts/pre_commit_check.sh        # staged files only
```

#### VS Code Integration
- **Command Palette**: Ctrl/Cmd+Shift+P → "Tasks: Run Task" → "pre-commit: Run All Checks"

### Skipping Hooks (Not Recommended)

```bash
# Skip all hooks (emergency only)
git commit --no-verify -m "emergency fix"

# Skip specific hook
SKIP=mypy git commit -m "skip mypy for this commit"
```

### Troubleshooting

#### Hook Installation Issues
```bash
# Reinstall hooks
uv run pre-commit uninstall
uv run pre-commit install

# Update hook repositories
uv run pre-commit autoupdate
```

#### Performance Issues
```bash
# Run hooks in parallel (faster)
uv run pre-commit run --all-files --parallel

# Clear cache if needed
uv run pre-commit clean
```

#### Common Fixes

**MyPy Errors**:
- Add type hints to functions
- Import proper types from `typing`
- Use `# type: ignore[error-code]` for known issues

**Ruff Errors**:
- Most are auto-fixed
- Check `pyproject.toml` for configuration
- Use `# ruff: noqa: E501` to ignore specific lines

**Bandit Warnings**:
- Review security implications
- Use `# nosec` comment if intentional
- Configure exclusions in `pyproject.toml`

## Continuous Integration

When setting up CI/CD, include these checks:

```yaml
# GitHub Actions example
- name: Run pre-commit
  run: |
    uv run pre-commit run --all-files
```

This ensures the same quality standards in your CI pipeline.

## Configuration Files

- **`.pre-commit-config.yaml`**: Pre-commit hook configuration
- **`pyproject.toml`**: Tool configurations (ruff, bandit, mypy)
- **`scripts/pre_commit_check.sh`**: Convenience script for manual runs

## Best Practices

1. **Run checks before pushing**: `./scripts/pre_commit_check.sh all`
2. **Fix issues immediately**: Don't accumulate technical debt
3. **Understand the tools**: Learn what each check does
4. **Configure appropriately**: Adjust rules in `pyproject.toml` as needed
5. **Keep dependencies updated**: Run `uv run pre-commit autoupdate` periodically

This ensures consistent, high-quality code across the entire team! 🚀

## Schema Organization & Development

### Pydantic v2 Schema Standards

This project follows domain-driven schema organization using Pydantic v2. All schemas are organized by business domain rather than by type (request/response).

#### Schema Directory Structure

```
src/schemas/
├── __init__.py              # Main exports - import all schemas here
├── common.py               # Shared base models and utilities
├── types.py                # Custom Pydantic types and validators
├── health.py               # Health check schemas
├── limiter.py              # Rate limiting schemas
├── users.py                # User-related schemas (when added)
├── auth.py                 # Authentication schemas (when added)
└── [domain].py             # Other domain-specific schemas
```

#### Adding New Schemas

Follow these steps when adding new schemas to the project:

##### 1. Choose the Right File

**Domain-Specific Schemas** (Recommended):
- Create or use existing domain file: `src/schemas/users.py`, `src/schemas/orders.py`
- Group related request, response, and data models together

**Shared/Common Schemas**:
- Add to `src/schemas/common.py` for base classes and utilities
- Add to `src/schemas/types.py` for custom types and validators

##### 2. Schema Naming Conventions

```python
# ✅ Good naming examples
class UserCreateRequest(BaseModel):      # Request models
class UserResponse(BaseModel):           # Response models
class UserUpdateRequest(BaseModel):      # Update requests
class UserListResponse(BaseModel):       # List responses
class UserSearchFilters(BaseModel):      # Filter models

# ❌ Avoid these patterns
class User(BaseModel):                   # Too generic
class UserModel(BaseModel):              # Redundant suffix
class CreateUser(BaseModel):             # Inconsistent order
```

##### 3. Domain Schema Template

When creating a new domain file (e.g., `src/schemas/users.py`):

```python
"""User-related Pydantic schemas."""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from .common import BaseResponse, PaginatedResponse


# Base user model (shared fields)
class UserBase(BaseModel):
    """Base user model with common fields."""

    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr = Field(description="User's email address")
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)


# Request models
class UserCreateRequest(UserBase):
    """Schema for creating a new user."""

    password: str = Field(min_length=8, max_length=128, description="User password")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepassword123"
            }
        }
    }


class UserUpdateRequest(BaseModel):
    """Schema for updating user information."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


# Response models
class UserResponse(UserBase):
    """Schema for user response data."""

    id: UUID = Field(description="Unique user identifier")
    is_active: bool = Field(default=True, description="Whether user is active")
    created_at: datetime = Field(description="When user was created")
    updated_at: datetime = Field(description="When user was last updated")

    model_config = {
        "from_attributes": True,  # Enable ORM mode for SQLAlchemy
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True,
                "created_at": "2025-01-09T12:00:00Z",
                "updated_at": "2025-01-09T12:00:00Z"
            }
        }
    }


class UserListResponse(PaginatedResponse[UserResponse]):
    """Paginated response for user lists."""
    pass
```

##### 4. Update Schema Exports

Always add new schemas to `src/schemas/__init__.py`:

```python
"""
Pydantic schemas for the FastAPI application.
"""

# Health schemas
from .health import HealthResponse

# Rate limiting schemas
from .limiter import RateLimitExceededResponse

# User schemas (example)
from .users import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse,
    UserListResponse
)

# Common schemas
from .common import BaseResponse, PaginatedResponse, ErrorResponse

__all__ = [
    # Health
    "HealthResponse",
    # Rate limiting
    "RateLimitExceededResponse",
    # Users
    "UserCreateRequest",
    "UserUpdateRequest",
    "UserResponse",
    "UserListResponse",
    # Common
    "BaseResponse",
    "PaginatedResponse",
    "ErrorResponse",
]
```

##### 5. Router Integration

Use schemas in your routers:

```python
from fastapi import APIRouter, HTTPException
from src.schemas import UserCreateRequest, UserResponse, UserListResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreateRequest) -> UserResponse:
    """Create a new user."""
    # Implementation here
    pass

@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = 1,
    size: int = 20
) -> UserListResponse:
    """List users with pagination."""
    # Implementation here
    pass
```

#### Best Practices Checklist

When creating schemas, ensure you:

- [ ] **Use descriptive names** with proper suffixes (`Request`, `Response`)
- [ ] **Add docstrings** to all classes and important fields
- [ ] **Include field descriptions** using `Field(description="...")`
- [ ] **Add validation** with `Field` constraints (min_length, max_length, gt, etc.)
- [ ] **Provide examples** using `model_config` with `json_schema_extra`
- [ ] **Use type hints** properly (`Optional`, `List[T]`, `Literal`)
- [ ] **Inherit from base models** when appropriate
- [ ] **Export in `__init__.py`** for easy imports
- [ ] **Follow naming conventions** consistently
- [ ] **Add custom validators** when needed using `@field_validator`

#### Common Patterns

**Pagination Response**:
```python
from .common import PaginatedResponse

class ProductListResponse(PaginatedResponse[ProductResponse]):
    """Paginated list of products."""
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

**Error Responses**:
```python
from .common import ErrorResponse

# Use the common ErrorResponse model
# No need to create domain-specific error models
```

Following these standards ensures consistency, maintainability, and excellent developer experience across the entire team! 🚀
