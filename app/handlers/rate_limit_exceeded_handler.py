import logging

from fastapi import Request, Response
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse

from app.schemas.rate_limit_exceeded_response import RateLimitExceededResponse

logger = logging.getLogger(__name__)


def rate_limit_exceeded_handler(request: Request, exc: Exception) -> Response:
    """
    Custom handler for managing requests that exceed rate limits.

    When a client exceeds the configured rate limits, this handler is invoked to
    return a 429 Too Many Requests response along with the `Retry-After` header
    indicating when the client can retry.

    Args:
        request (Request): The incoming HTTP request that triggered the rate limiter.
        exc (RateLimitExceeded): The exception raised when the rate limit is exceeded.

    Returns:
        Response: A JSON response with status code 429, a Retry-After header,
                  and a detailed message in the body.
    """
    if isinstance(exc, RateLimitExceeded):
        client_host = request.client.host if request.client is not None else "unknown"
        logger.info("Rate limiter triggered by %s", client_host)

        retry_after_seconds = getattr(
            getattr(getattr(exc, "limit", None), "GRANULARITY", None), "seconds", 1
        )

        response_body = RateLimitExceededResponse(
            retry_after_seconds=retry_after_seconds
        )

        response = JSONResponse(
            status_code=429,
            content=response_body.model_dump(),
            headers={"Retry-After": str(retry_after_seconds)},
        )

        if hasattr(request.app.state.limiter, "inject_headers"):
            response = request.app.state.limiter.inject_headers(
                response, request.state.view_rate_limit
            )

        return response
    else:
        raise exc
