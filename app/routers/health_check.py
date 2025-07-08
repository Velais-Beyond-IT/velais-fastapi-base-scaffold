import logging
from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.configuration.limiter import limiter
from app.models.responses.health_response import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
@limiter.exempt
async def health(request: Request):
    """
    Health check endpoint.

    Returns a 200 OK response with application health status.
    Logs the client host making the request.

    Args:
        request (Request): The incoming HTTP request object.

    Returns:
        JSONResponse: A JSON response containing health status information.
    """
    client_host = request.client.host if request.client else "unknown"
    logger.info("Health check request from %s", client_host)
    content = HealthResponse()
    response = JSONResponse(
        status_code=200,
        content=content.model_dump(),
    )
    return response
