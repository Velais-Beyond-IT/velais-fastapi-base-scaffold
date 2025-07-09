"""
Pydantic schemas for the FastAPI application.

Schemas are organized by domain/feature area for better maintainability.
Each domain module contains related request, response, and data models.
"""

from .health import HealthResponse
from .limiter import RateLimitExceededResponse

__all__ = [
    # Health
    "HealthResponse",
    # Rate Limiter
    "RateLimitExceededResponse",
]
