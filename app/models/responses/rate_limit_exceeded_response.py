from pydantic import BaseModel


class RateLimitExceededResponse(BaseModel):
    detail: str = "Rate limit exceeded. Please try again later."
    retry_after_seconds: int
