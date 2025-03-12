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
    logger.info(f"Health check request from {request.client.host}")
    content = HealthResponse()
    response = JSONResponse(
        status_code=200,
        content=content.model_dump(),
    )
    return response
