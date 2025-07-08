#!/bin/bash
# Type checking script for development workflow
echo "🔍 Running mypy type checker..."
uv run mypy app/
MYPY_EXIT_CODE=$?

if [ $MYPY_EXIT_CODE -eq 0 ]; then
    echo "✅ Type checking passed!"
else
    echo "❌ Type checking failed!"
    exit 1
fi
