from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str = Field(
        default="healthy", description="Current health status of the application"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when health check was performed",
    )
