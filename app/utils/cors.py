"""CORS configuration utilities."""

import re


def validate_origin(origin: str) -> bool:
    """Validate if an origin URL is properly formatted."""
    if origin == "*":
        return True

    # Basic URL validation
    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)*[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?)"  # domain
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return bool(url_pattern.match(origin))


def parse_cors_origins(
    origins_string: str, environment: str = "development"
) -> list[str]:
    """Parse CORS origins string into a list with environment-specific handling."""
    if origins_string == "*":
        # Only allow wildcard in development
        return ["*"] if environment == "development" else []

    origins = []
    for origin in origins_string.split(","):
        origin = origin.strip()
        if origin and validate_origin(origin):
            origins.append(origin)

    return origins


def is_cors_secure(origins: list[str], environment: str) -> bool:
    """Check if CORS configuration is secure for the given environment."""
    if environment == "development":
        return True  # Allow any configuration in development

    # In production/staging, wildcard is not secure
    if "*" in origins:
        return False

    # All origins should use HTTPS in production
    if environment == "production":
        for origin in origins:
            if origin.startswith("http://") and not origin.startswith(
                "http://localhost"
            ):
                return False

    return True
