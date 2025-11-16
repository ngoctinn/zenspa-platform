"""Redis cache helpers với hỗ trợ fallback."""

import json
from typing import Any
from redis.exceptions import ConnectionError as RedisConnectionError

from app.redis.client import get_redis_client
from app.core.logging import logger


def cache_get(key: str, fallback: Any = None) -> Any:
    """
    Lấy giá trị từ cache với fallback.

    Nếu Redis unavailable, trả về giá trị fallback.

    Args:
        key: Cache key
        fallback: Giá trị trả về nếu cache miss hoặc Redis down

    Returns:
        Giá trị cached hoặc fallback
    """
    try:
        redis = get_redis_client()
        if redis is None:
            logger.warning(f"Redis unavailable, trả về fallback cho {key}")
            return fallback

        value = redis.get(key)
        if value is None:
            return fallback

        # Thử parse JSON, fallback về string
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    except RedisConnectionError:
        logger.warning(f"Lỗi kết nối Redis, trả về fallback cho {key}")
        return fallback
    except Exception as e:
        logger.error(f"Lỗi cache: {e}, trả về fallback")
        return fallback


def cache_set(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Lưu giá trị vào cache.

    Args:
        key: Cache key
        value: Giá trị để cache (sẽ được JSON serialize)
        ttl: Thời gian sống tính bằng giây

    Returns:
        True nếu thành công, False nếu Redis unavailable
    """
    try:
        redis = get_redis_client()
        if redis is None:
            logger.warning(f"Redis unavailable, bỏ qua cache set cho {key}")
            return False

        # Serialize giá trị thành JSON
        try:
            serialized_value = json.dumps(value)
        except (TypeError, ValueError):
            # Nếu không thể serialize, chuyển thành string
            serialized_value = str(value)

        redis.setex(key, ttl, serialized_value)
        return True

    except Exception as e:
        logger.error(f"Lỗi cache set: {e}")
        return False


def cache_delete(key: str) -> bool:
    """
    Xóa giá trị khỏi cache.

    Args:
        key: Cache key cần xóa

    Returns:
        True nếu thành công, False nếu Redis unavailable
    """
    try:
        redis = get_redis_client()
        if redis is None:
            logger.warning(f"Redis unavailable, bỏ qua cache delete cho {key}")
            return False

        redis.delete(key)
        return True

    except Exception as e:
        logger.error(f"Lỗi cache delete: {e}")
        return False


def cache_exists(key: str) -> bool:
    """
    Kiểm tra key có tồn tại trong cache không.

    Args:
        key: Cache key cần kiểm tra

    Returns:
        True nếu tồn tại, False nếu không hoặc Redis unavailable
    """
    try:
        redis = get_redis_client()
        if redis is None:
            return False

        return bool(redis.exists(key))

    except Exception as e:
        logger.error(f"Lỗi kiểm tra cache exists: {e}")
        return False
