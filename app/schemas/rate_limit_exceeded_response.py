from pydantic import BaseModel, Field


class RateLimitExceededResponse(BaseModel):
    """Response schema for rate limit exceeded errors."""

    detail: str = Field(
        default="Rate limit exceeded. Please try again later.",
        description="Error message describing the rate limit violation",
    )
    retry_after_seconds: int = Field(
        description="Number of seconds to wait before retrying the request", gt=0
    )
