"""Quản lý kết nối Redis."""

import redis
from redis.exceptions import ConnectionError as RedisConnectionError
from app.core.config import settings
from app.core.exceptions import CacheException
from app.core.logging import logger


# Instance client Redis toàn cục
_redis_client: redis.Redis | None = None


def get_redis_client() -> redis.Redis | None:
    """Lấy instance client Redis với lazy initialization."""
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password,
                decode_responses=settings.redis_decode_responses,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
            )
            # Test kết nối
            _redis_client.ping()
            logger.info("✅ Kết nối Redis thành công")
        except RedisConnectionError as e:
            logger.warning(f"❌ Kết nối Redis thất bại: {e}")
            _redis_client = None
        except Exception as e:
            logger.error(f"Lỗi khởi tạo Redis: {e}")
            _redis_client = None

    return _redis_client


def check_redis_health() -> tuple[bool, float]:
    """
    Kiểm tra sức khỏe Redis bằng cách ping server.

    Trả về:
        tuple: (is_healthy: bool, response_time: float tính bằng giây)
    """
    import time
    start_time = time.time()
    try:
        client = get_redis_client()
        if client is None:
            return False, 0.0

        client.ping()
        response_time = time.time() - start_time
        logger.debug(f"Health check Redis thành công trong {response_time:.3f}s")
        return True, response_time
    except Exception as e:
        response_time = time.time() - start_time
        logger.error(f"Health check Redis thất bại: {e}")
        return False, response_time


def close_redis() -> None:
    """Đóng kết nối Redis."""
    global _redis_client
    if _redis_client:
        _redis_client.close()
        _redis_client = None
        logger.info("Kết nối Redis đã đóng")
