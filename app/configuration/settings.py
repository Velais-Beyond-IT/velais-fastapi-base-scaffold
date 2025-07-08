from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration class for managing application settings.

    This class uses `pydantic.BaseSettings` to load environment variables and validate them.
    All configurable settings for the application should be defined here.

    Attributes:
        env (str): Application environment (e.g., development or production).
        rate_limiter (str): Configuration for rate limiting (e.g., "5/minute").
    """

    env: str = "development"
    rate_limiter: str = "5/minute"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    """
    Retrieve the application settings instance.

    This function caches the settings instance to ensure it's only initialized once (singleton),
    improving performance and maintaining consistency across the application.

    Returns:
        Settings: The cached settings instance.
    """
    return Settings()


settings = get_settings()
