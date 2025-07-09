from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration class for managing application settings.

    This class uses `pydantic.BaseSettings` to load environment variables and validate them.
    All configurable settings for the application should be defined here.

    Attributes:
        env (str): Application environment (e.g., development, staging, production).
        rate_limiter (str): Configuration for rate limiting (e.g., "60/minute").
        cors_origins (str): Comma-separated list of allowed CORS origins.
        cors_allow_credentials (bool): Whether to allow credentials in CORS requests.
        cors_allow_methods (str): Comma-separated list of allowed HTTP methods.
        cors_allow_headers (str): Comma-separated list of allowed headers.
        cors_max_age (int): Maximum age for CORS preflight cache in seconds.
    """

    # Environment
    env: str = "development"

    # Rate Limiting
    rate_limiter: str = "60/minute"

    # CORS Configuration
    cors_origins: str = "*"
    cors_allow_credentials: bool = True
    cors_allow_methods: str = "GET,POST,PUT,DELETE,OPTIONS,PATCH"
    cors_allow_headers: str = "*"
    cors_max_age: int = 86400

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, v: str) -> str:
        """Validate CORS origins format."""
        if v == "*":
            return v

        # Basic validation for URL format
        origins = [origin.strip() for origin in v.split(",")]
        for origin in origins:
            if origin and not (
                origin.startswith("http://") or origin.startswith("https://")
            ):
                raise ValueError(
                    f"Invalid origin format: {origin}. Must start with http:// or https://"
                )

        return v

    def get_cors_origins(self) -> list[str]:
        """Get parsed CORS origins as a list."""
        if self.cors_origins == "*":
            return ["*"] if self.env == "development" else []

        origins = [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]
        return origins

    def get_cors_methods(self) -> list[str]:
        """Get parsed CORS methods as a list."""
        if self.cors_allow_methods == "*":
            return ["*"]
        return [
            method.strip()
            for method in self.cors_allow_methods.split(",")
            if method.strip()
        ]

    def get_cors_headers(self) -> list[str]:
        """Get parsed CORS headers as a list."""
        if self.cors_allow_headers == "*":
            return ["*"]
        return [
            header.strip()
            for header in self.cors_allow_headers.split(",")
            if header.strip()
        ]


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
