"""Tests for Redis layer."""

import pytest
from unittest.mock import patch, MagicMock
from app.redis.client import check_redis_health
from app.redis.helpers import cache_get, cache_set, cache_delete


def test_check_redis_health_success():
    """Test successful Redis health check."""
    with patch('app.redis.client.get_redis_client') as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.ping.return_value = True

        is_healthy, response_time = check_redis_health()

        assert is_healthy is True
        assert response_time >= 0


def test_check_redis_health_failure():
    """Test failed Redis health check."""
    with patch('app.redis.client.get_redis_client') as mock_get_client:
        mock_get_client.return_value = None

        is_healthy, response_time = check_redis_health()

        assert is_healthy is False
        assert response_time == 0.0


def test_cache_get_success():
    """Test successful cache get."""
    with patch('app.redis.helpers.get_redis_client') as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = '{"key": "value"}'

        result = cache_get("test_key")

        assert result == {"key": "value"}


def test_cache_get_fallback():
    """Test cache get with fallback."""
    with patch('app.redis.helpers.get_redis_client') as mock_get_client:
        mock_get_client.return_value = None

        result = cache_get("test_key", fallback="default")

        assert result == "default"


def test_cache_set_success():
    """Test successful cache set."""
    with patch('app.redis.helpers.get_redis_client') as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = cache_set("test_key", "test_value", ttl=3600)

        assert result is True
        mock_client.setex.assert_called_once()


def test_cache_set_fallback():
    """Test cache set with Redis unavailable."""
    with patch('app.redis.helpers.get_redis_client') as mock_get_client:
        mock_get_client.return_value = None

        result = cache_set("test_key", "test_value")

        assert result is False
