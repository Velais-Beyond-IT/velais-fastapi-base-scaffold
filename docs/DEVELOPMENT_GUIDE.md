# Development Guide

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
