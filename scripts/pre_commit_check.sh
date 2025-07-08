#!/bin/bash
# Pre-commit quality checks script for development workflow
echo "🔍 Running pre-commit checks..."

# Run pre-commit on all files or just staged files
if [ "$1" = "all" ]; then
    echo "Running on all files..."
    uv run pre-commit run --all-files
else
    echo "Running on staged files..."
    uv run pre-commit run
fi

PRECOMMIT_EXIT_CODE=$?

if [ $PRECOMMIT_EXIT_CODE -eq 0 ]; then
    echo "✅ All pre-commit checks passed!"
else
    echo "❌ Some pre-commit checks failed!"
    echo "💡 Tip: Files may have been auto-fixed. Review changes and commit again."
    exit 1
fi
