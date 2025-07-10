"""
Test configuration for the FastAPI application.

This module sets up the test environment and provides common fixtures
for testing the application.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
app_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(app_dir.parent))
