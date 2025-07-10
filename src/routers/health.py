import logging

from fastapi import APIRouter, Request

from src.config.limiter import limiter
from src.schemas import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
@limiter.exempt  # type: ignore[misc]
async def health(request: Request) -> HealthResponse:
    """
    Health check endpoint.

    Returns a 200 OK response with application health status.
    Logs the client host making the request.

    Args:
        request (Request): The incoming HTTP request object.

    Returns:
        HealthResponse: A response containing health status information.
    """
    client_host = request.client.host if request.client else "unknown"
    logger.info("Health check request from %s", client_host)

    return HealthResponse()
