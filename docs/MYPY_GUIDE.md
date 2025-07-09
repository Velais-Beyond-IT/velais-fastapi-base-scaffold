# MyPy Integration Guide

## Overview
This project uses mypy for static type checking to ensure code quality and catch potential bugs before runtime.

## Configuration
MyPy is configured in `pyproject.toml` with:
- Strict type checking enabled
- Pydantic v2 plugin for better validation
- Custom overrides for third-party libraries
- Relaxed rules for test files

## Running Type Checks

### Command Line
```bash
# Check all app code
uv run mypy app/

# Check specific file
uv run mypy app/routers/health.py

# Check with verbose output
uv run mypy app/ --verbose
```

### VS Code
- Use Ctrl/Cmd+Shift+P → "Tasks: Run Task" → "mypy: Type Check"
- Or use the provided script: `./scripts/type_check.sh`

### Pre-commit Hook (Recommended)
Add to your development workflow:
```bash
./scripts/type_check.sh && uv run pytest
```

## Common Type Issues & Solutions

### 1. Untyped Decorators
```python
# Problem
@some_decorator
def my_function(): ...

# Solution
@some_decorator  # type: ignore[misc]
def my_function(): ...
```

### 2. Missing Type Annotations
```python
# Problem
def process_data(data):
    return data.upper()

# Solution
def process_data(data: str) -> str:
    return data.upper()
```

### 3. Optional Types
```python
# Problem
def get_user(user_id):
    if user_id:
        return User(user_id)
    return None

# Solution
from typing import Optional

def get_user(user_id: int) -> Optional[User]:
    if user_id:
        return User(user_id)
    return None
```

### 4. Pydantic Models
```python
# Always include proper type hints
class UserSchema(BaseModel):
    name: str = Field(description="User's full name")
    age: int = Field(gt=0, description="User's age")
    email: Optional[str] = Field(None, description="User's email")
```

## Best Practices

1. **Always add type hints** to function parameters and return values
2. **Use strict mode** for new code (already configured)
3. **Add `# type: ignore[error-code]`** only when necessary with specific error codes
4. **Use `typing` module** for complex types (Union, Optional, List, Dict)
5. **Validate with mypy** before committing code

## Integration with CI/CD

Add to your GitHub Actions or similar:
```yaml
- name: Type check with mypy
  run: uv run mypy app/
```

## Troubleshooting

### Import Errors
If mypy can't find imports, add them to the overrides in `pyproject.toml`:
```toml
[[tool.mypy.overrides]]
module = ["your_module.*"]
ignore_missing_imports = true
```

### Performance Issues
For large codebases, use:
```bash
uv run mypy app/ --cache-dir=.mypy_cache
```

This ensures type safety and better code quality throughout the development process.
