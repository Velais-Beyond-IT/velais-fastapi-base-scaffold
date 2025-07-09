import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.config.limiter import limiter
from app.config.settings import settings
from app.handlers.rate_limit_exceeded import rate_limit_exceeded_handler
from app.routers import health

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create a logger
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator[None]:
    """Manage application lifespan events."""
    # Startup
    logger.info("🚀 Starting %s", app_instance.title)
    logger.info("Environment: %s", settings.env)
    logger.info("CORS Origins: %s", settings.get_cors_origins())
    logger.info("CORS Methods: %s", settings.get_cors_methods())
    logger.info("CORS Headers: %s", settings.get_cors_headers())
    logger.info("CORS Allow Credentials: %s", settings.cors_allow_credentials)
    logger.info("CORS Max Age: %s seconds", settings.cors_max_age)
    logger.info("Rate Limiter: %s", settings.rate_limiter)
    logger.info(
        "Documentation URL: %s",
        "/docs" if settings.env == "development" else "disabled",
    )
    logger.info("✅ Application startup complete")

    yield

    # Shutdown
    logger.info("🛑 Application shutdown complete")


app = FastAPI(
    title="<Application Title>",
    description="""
    <Application Description>
    """,
    version="1.0.0",
    lifespan=lifespan,
    redoc_url=None,
    docs_url="/docs" if settings.env == "development" else None,
)

# Add CORS middleware with environment-specific configuration
cors_origins = settings.get_cors_origins()
cors_methods = settings.get_cors_methods()
cors_headers = settings.get_cors_headers()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=cors_methods,
    allow_headers=cors_headers,
    max_age=settings.cors_max_age,
)

# Add the Limiter middleware with the custom handler
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Add API routes
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
