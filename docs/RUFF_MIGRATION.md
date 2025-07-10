# Ruff Migration Guide

## 🚀 What Changed

We've migrated from **multiple legacy tools** to **Ruff** for all Python linting and formatting:

### Before (Legacy)
```bash
# Multiple tools needed
pip install pylint black isort flake8 pyupgrade
pylint src/                    # ~30 seconds
black src/                     # ~10 seconds
isort src/                     # ~5 seconds
flake8 src/                    # ~15 seconds
```

### After (Ruff)
```bash
# Single tool does it all
uv add --dev ruff
uv run ruff check src/         # ~0.1 seconds
uv run ruff format src/        # ~0.1 seconds
```

## 🔄 Command Migration

| Old Command | New Ruff Command |
|-------------|------------------|
| `pylint src/` | `uv run ruff check src/` |
| `black src/` | `uv run ruff format src/` |
| `black --check src/` | `uv run ruff format --check src/` |
| `isort src/` | `uv run ruff check --fix src/` (I rules) |
| `flake8 src/` | `uv run ruff check src/` |

## 🛠️ VS Code Setup

### Required Extension
- **Install**: `charliermarsh.ruff`
- **Remove**: `ms-python.pylint`, `ms-python.black-formatter`

### Automatic Configuration
The project `.vscode/settings.json` automatically:
- Uses Ruff as the default formatter
- Runs Ruff on save
- Organizes imports on save
- Shows linting errors in real-time

## ⚡ Speed Comparison

| Tool | Time | Files Checked |
|------|------|---------------|
| **Legacy Stack** | ~60s | All Python files |
| **Ruff** | ~0.1s | All Python files |

**Result**: 100-600x faster! 🚀

## 🎯 Benefits

### For Developers
- **Instant feedback** in VS Code
- **Auto-fixing** of many issues
- **Consistent formatting** across team
- **No more tool conflicts**

### For CI/CD
- **Faster pre-commit hooks** (60s → <1s)
- **Simpler configuration**
- **Single dependency** to manage
- **Better error messages**

## 📚 Learning Ruff

### Most Common Commands
```bash
# Check all files for issues
uv run ruff check

# Auto-fix what can be fixed
uv run ruff check --fix

# Format all Python files
uv run ruff format

# Check if formatting is needed
uv run ruff format --check

# Run both check and format
uv run ruff check --fix && uv run ruff format
```

### VS Code Shortcuts
- **Ctrl/Cmd + Shift + P** → "Format Document" (Ruff format)
- **Ctrl/Cmd + Shift + P** → "Organize Imports" (Ruff import sorting)
- Issues show automatically in "Problems" panel

## 🔧 Configuration

All Ruff configuration is in `pyproject.toml`:
```toml
[tool.ruff]
target-version = "py313"
line-length = 88
fix = true

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM"]
```

## 🚨 Troubleshooting

### "Ruff not found"
```bash
# Install with uv
uv add --dev ruff

# Or reinstall the VS Code extension
```

### "Legacy tool still running"
```bash
# Remove old extensions in VS Code:
# - ms-python.pylint
# - ms-python.black-formatter
# - ms-python.isort
```

### "Different formatting than before"
This is expected! Ruff uses more modern formatting standards. The team should:
1. Run `uv run ruff format` on the entire codebase once
2. Commit the formatting changes
3. Everyone pulls the changes

Now everyone will have consistent formatting! ✨
