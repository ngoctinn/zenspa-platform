"""
Redis connection and caching utilities.
Includes graceful fallback when Redis is unavailable.
"""

import logging
from typing import Any

from redis import asyncio as aioredis
from redis.exceptions import RedisError

from app.core.config import settings
from app.core.exceptions import ErrorCode, RedisException

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client with graceful fallback."""

    def __init__(self) -> None:
        """Initialize Redis client."""
        self._redis: aioredis.Redis | None = None
        self._available = False

    async def connect(self) -> None:
        """
        Connect to Redis.

        Note: Does not raise exception if connection fails.
        Sets _available to False for graceful degradation.
        """
        try:
            logger.info("Connecting to Redis...")

            # Create Redis connection
            self._redis = await aioredis.from_url(
                f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
                password=settings.redis_password if settings.redis_password else None,
                decode_responses=settings.redis_decode_responses,
                socket_connect_timeout=5,
                socket_timeout=5,
            )

            # Test connection
            await self._redis.ping()
            self._available = True

            logger.info("Redis connected successfully")

        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Running without cache.")
            self._available = False
            self._redis = None

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._redis:
            logger.info("Disconnecting from Redis...")
            await self._redis.close()
            self._redis = None
            self._available = False
            logger.info("Redis disconnected")

    async def get(self, key: str) -> str | None:
        """
        Get value from Redis.

        Args:
            key: Cache key

        Returns:
            str | None: Cached value or None if not found or Redis unavailable
        """
        if not self._available or not self._redis:
            return None

        try:
            return await self._redis.get(key)
        except RedisError as e:
            logger.warning(f"Redis GET failed for key '{key}': {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        expire: int | None = None,
    ) -> bool:
        """
        Set value in Redis.

        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds (optional)

        Returns:
            bool: True if successful, False otherwise
        """
        if not self._available or not self._redis:
            return False

        try:
            await self._redis.set(key, value, ex=expire)
            return True
        except RedisError as e:
            logger.warning(f"Redis SET failed for key '{key}': {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete key from Redis.

        Args:
            key: Cache key

        Returns:
            bool: True if successful, False otherwise
        """
        if not self._available or not self._redis:
            return False

        try:
            await self._redis.delete(key)
            return True
        except RedisError as e:
            logger.warning(f"Redis DELETE failed for key '{key}': {e}")
            return False

    async def exists(self, key: str) -> bool:
        """
        Check if key exists in Redis.

        Args:
            key: Cache key

        Returns:
            bool: True if exists, False otherwise
        """
        if not self._available or not self._redis:
            return False

        try:
            return bool(await self._redis.exists(key))
        except RedisError as e:
            logger.warning(f"Redis EXISTS failed for key '{key}': {e}")
            return False

    async def health_check(self) -> bool:
        """
        Check Redis health.

        Returns:
            bool: True if Redis is healthy
        """
        if not self._available or not self._redis:
            return False

        try:
            await self._redis.ping()
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            self._available = False
            return False

    @property
    def is_available(self) -> bool:
        """Check if Redis is available."""
        return self._available


# Global Redis instance
redis_client = RedisClient()
