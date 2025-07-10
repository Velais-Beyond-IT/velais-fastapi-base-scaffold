from slowapi import Limiter
from slowapi.util import get_remote_address

from src.config.settings import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.rate_limiter],
)
