"""Tests for CORS configuration."""

import pytest

from app.config.settings import Settings
from app.utils.cors import is_cors_secure, parse_cors_origins, validate_origin


def test_validate_origin():
    """Test origin validation."""
    # Valid origins
    assert validate_origin("*") is True
    assert validate_origin("https://example.com") is True
    assert validate_origin("http://localhost:3000") is True
    assert validate_origin("https://subdomain.example.com") is True
    assert validate_origin("https://example.com:8080") is True

    # Invalid origins
    assert validate_origin("invalid-url") is False
    assert validate_origin("ftp://example.com") is False
    assert validate_origin("") is False


def test_parse_cors_origins():
    """Test CORS origins parsing."""
    # Development allows wildcard
    assert parse_cors_origins("*", "development") == ["*"]

    # Production doesn't allow wildcard
    assert parse_cors_origins("*", "production") == []

    # Multiple origins
    origins = "https://app.com,https://admin.app.com"
    expected = ["https://app.com", "https://admin.app.com"]
    assert parse_cors_origins(origins, "production") == expected

    # Origins with spaces
    origins_with_spaces = " https://app.com , https://admin.app.com "
    assert parse_cors_origins(origins_with_spaces, "production") == expected

    # Mixed valid and invalid origins
    mixed_origins = "https://valid.com,invalid-url,https://another-valid.com"
    expected_mixed = ["https://valid.com", "https://another-valid.com"]
    assert parse_cors_origins(mixed_origins, "production") == expected_mixed


def test_is_cors_secure():
    """Test CORS security validation."""
    # Development is always secure
    assert is_cors_secure(["*"], "development") is True
    assert is_cors_secure(["http://insecure.com"], "development") is True

    # Production with wildcard is not secure
    assert is_cors_secure(["*"], "production") is False

    # Production with HTTPS origins is secure
    assert is_cors_secure(["https://app.com"], "production") is True

    # Production with HTTP (non-localhost) is not secure
    assert is_cors_secure(["http://app.com"], "production") is False

    # Localhost HTTP is allowed in production
    assert is_cors_secure(["http://localhost:3000"], "production") is True

    # Staging with wildcard is not secure
    assert is_cors_secure(["*"], "staging") is False

    # Staging with HTTPS is secure
    assert is_cors_secure(["https://staging.app.com"], "staging") is True


def test_settings_cors_validation():
    """Test settings CORS validation."""
    # Valid CORS configuration
    settings = Settings(cors_origins="https://example.com,https://admin.example.com")
    origins = settings.get_cors_origins()
    assert len(origins) == 2
    assert "https://example.com" in origins
    assert "https://admin.example.com" in origins

    # Wildcard in development
    dev_settings = Settings(env="development", cors_origins="*")
    dev_origins = dev_settings.get_cors_origins()
    assert dev_origins == ["*"]

    # Wildcard in production returns empty list
    prod_settings = Settings(env="production", cors_origins="*")
    prod_origins = prod_settings.get_cors_origins()
    assert prod_origins == []


def test_settings_cors_methods():
    """Test CORS methods parsing."""
    settings = Settings(cors_allow_methods="GET,POST,PUT")
    methods = settings.get_cors_methods()
    assert methods == ["GET", "POST", "PUT"]

    # Wildcard methods
    settings_wildcard = Settings(cors_allow_methods="*")
    methods_wildcard = settings_wildcard.get_cors_methods()
    assert methods_wildcard == ["*"]


def test_settings_cors_headers():
    """Test CORS headers parsing."""
    settings = Settings(cors_allow_headers="Authorization,Content-Type")
    headers = settings.get_cors_headers()
    assert headers == ["Authorization", "Content-Type"]

    # Wildcard headers
    settings_wildcard = Settings(cors_allow_headers="*")
    headers_wildcard = settings_wildcard.get_cors_headers()
    assert headers_wildcard == ["*"]


def test_cors_origins_validation_error():
    """Test CORS origins validation errors."""
    with pytest.raises(ValueError, match="Invalid origin format"):
        Settings(cors_origins="invalid-url")

    with pytest.raises(ValueError, match="Invalid origin format"):
        Settings(cors_origins="https://valid.com,invalid-url")


def test_environment_specific_defaults():
    """Test that different environments have appropriate defaults."""
    # Development environment
    dev_settings = Settings(env="development")
    dev_origins = dev_settings.get_cors_origins()
    assert dev_origins == ["*"]

    # Production environment
    prod_settings = Settings(env="production", cors_origins="https://prod.com")
    prod_origins = prod_settings.get_cors_origins()
    assert prod_origins == ["https://prod.com"]

    # Staging environment
    staging_settings = Settings(env="staging", cors_origins="https://staging.com")
    staging_origins = staging_settings.get_cors_origins()
    assert staging_origins == ["https://staging.com"]


def test_cors_configuration_integration():
    """Test complete CORS configuration integration."""
    # Production-like configuration
    settings = Settings(
        env="production",
        cors_origins="https://app.com,https://admin.app.com",
        cors_allow_methods="GET,POST,PUT,DELETE,OPTIONS",
        cors_allow_headers="Authorization,Content-Type,Accept",
        cors_allow_credentials=True,
        cors_max_age=3600,
    )

    origins = settings.get_cors_origins()
    methods = settings.get_cors_methods()
    headers = settings.get_cors_headers()

    # Verify parsed values
    assert origins == ["https://app.com", "https://admin.app.com"]
    assert methods == ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    assert headers == ["Authorization", "Content-Type", "Accept"]
    assert settings.cors_allow_credentials is True
    assert settings.cors_max_age == 3600

    # Verify security
    assert is_cors_secure(origins, settings.env) is True
