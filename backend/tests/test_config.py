"""Tests for configuration management."""

import pytest
from app.core.config import Settings


def test_settings_creation():
    """Test that settings can be created."""
    settings = Settings(
        database_url="postgresql://test:test@localhost/test",
        upstash_redis_rest_url="https://test.upstash.io",
        upstash_redis_rest_token="test_token"
    )
    assert settings.app_name == "ZenSpa Backend"
    assert settings.database_url == "postgresql://test:test@localhost/test"


def test_cors_origins_list():
    """Test CORS origins list property."""
    settings = Settings(
        database_url="postgresql://test:test@localhost/test",
        cors_origins=["http://localhost:3000", "https://example.com"]
    )
    assert settings.cors_origins_list == ["http://localhost:3000", "https://example.com"]


def test_database_url_validation():
    """Test database URL validation."""
    with pytest.raises(ValueError, match="DATABASE_URL must start with postgresql"):
        Settings(database_url="mysql://test:test@localhost/test")
