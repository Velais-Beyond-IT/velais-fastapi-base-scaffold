# Schema Development Quick Reference

## 🎯 Quick Checklist for New Schemas

### 1. File Organization
- [ ] Create domain-specific file: `app/schemas/[domain].py`
- [ ] Or add to existing: `app/schemas/common.py` or `app/schemas/types.py`

### 2. Naming Convention
- [ ] Use descriptive names: `UserCreateRequest`, `UserResponse`
- [ ] Add proper suffixes: `Request`, `Response`, `Filters`
- [ ] Avoid generic names: `User`, `Model`, `Schema`

### 3. Schema Structure
- [ ] Add class docstring
- [ ] Use `Field()` with descriptions
- [ ] Add validation constraints
- [ ] Include `json_schema_extra` examples
- [ ] Use proper type hints

### 4. Exports & Integration
- [ ] Add to `app/schemas/__init__.py` imports
- [ ] Add to `__all__` list
- [ ] Use in router with `response_model`

## 📝 Templates

### Basic Domain Schema
```python
"""[Domain] Pydantic schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class [Domain]Base(BaseModel):
    """Base [domain] model."""
    name: str = Field(min_length=1, max_length=100)

class [Domain]CreateRequest([Domain]Base):
    """Schema for creating [domain]."""
    model_config = {
        "json_schema_extra": {
            "example": {"name": "Example"}
        }
    }

class [Domain]Response([Domain]Base):
    """Schema for [domain] response."""
    id: UUID
    created_at: datetime
    model_config = {"from_attributes": True}
```

### With Validation
```python
from pydantic import field_validator

class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
```

### Pagination Response
```python
from .common import PaginatedResponse

class [Domain]ListResponse(PaginatedResponse[[Domain]Response]):
    """Paginated list of [domain] items."""
    pass
```

## 🔗 Common Imports

```python
# Standard library
from datetime import datetime
from typing import Optional, List, Literal
from uuid import UUID

# Pydantic
from pydantic import BaseModel, Field, EmailStr, field_validator

# Project schemas
from .common import BaseResponse, PaginatedResponse, ErrorResponse
```

## 🚫 What NOT to Do

```python
# ❌ No docstrings
class User(BaseModel):
    name: str

# ❌ No field descriptions
class UserRequest(BaseModel):
    name: str = Field(min_length=1)

# ❌ Generic names
class Model(BaseModel):
    pass

# ❌ Wrong naming order
class CreateUser(BaseModel):
    pass

# ❌ Missing examples
class UserResponse(BaseModel):
    id: UUID
    name: str
    # No model_config with examples

# ❌ Not exported
# Creating schema but forgetting to add to __init__.py
```

## ✅ Complete Example

```python
"""User-related Pydantic schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, field_validator

from .common import PaginatedResponse


class UserBase(BaseModel):
    """Base user model with shared fields."""

    username: str = Field(
        min_length=3,
        max_length=50,
        description="Unique username"
    )
    email: EmailStr = Field(description="User's email address")
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v.lower()


class UserCreateRequest(UserBase):
    """Schema for creating a new user."""

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password"
    )

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


class UserResponse(UserBase):
    """Schema for user response data."""

    id: UUID = Field(description="Unique user identifier")
    is_active: bool = Field(default=True, description="Whether user is active")
    created_at: datetime = Field(description="When user was created")
    updated_at: datetime = Field(description="When user was last updated")

    model_config = {
        "from_attributes": True,  # Enable ORM mode
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

## 📖 More Information

- **Detailed Guide**: `docs/DEVELOPMENT_GUIDE.md`
- **Project README**: `README.md`
- **Pydantic v2 Docs**: https://docs.pydantic.dev/latest/
