"""Quản lý kết nối Redis với hỗ trợ REST API."""

import json
import time
from typing import Any
import requests
from app.core.config import settings
from app.core.exceptions import CacheException
from app.core.logging import logger


class UpstashRestClient:
    """Redis client sử dụng Upstash REST API."""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Thực hiện HTTP request đến Upstash REST API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Upstash REST API error: {e}")
            raise CacheException(f"Redis REST API error: {e}")

    def ping(self) -> str:
        """Test connection."""
        result = self._request("GET", "/ping")
        return result.get("result", "PONG")

    def get(self, key: str) -> str | None:
        """Get value by key."""
        result = self._request("GET", f"/get/{key}")
        return result.get("result")

    def setex(self, key: str, time: int, value: str) -> str | None:
        """Set key with expiration."""
        # Sử dụng format command array để xử lý ký tự đặc biệt trong value an toàn
        # POST / với body ["SETEX", key, str(time), value]
        result = self._request("POST", "/", json=["SETEX", key, str(time), value])
        return result.get("result")

    def delete(self, key: str) -> int:
        """Delete key."""
        result = self._request("POST", f"/del/{key}")
        return result.get("result", 0)

    def exists(self, key: str) -> int:
        """Check if key exists."""
        result = self._request("GET", f"/exists/{key}")
        return result.get("result", 0)

    def close(self) -> None:
        """Close session."""
        self.session.close()


# Instance client Redis toàn cục
_redis_client: UpstashRestClient | None = None


def get_redis_client() -> UpstashRestClient | None:
    """Lấy instance client Redis với lazy initialization."""
    global _redis_client
    if _redis_client is None:
        try:
            if settings.upstash_redis_rest_url and settings.upstash_redis_rest_token:
                # Use REST API
                _redis_client = UpstashRestClient(
                    settings.upstash_redis_rest_url, settings.upstash_redis_rest_token
                )
                # Test kết nối
                _redis_client.ping()
                logger.info("✅ Kết nối Upstash REST API thành công")
            else:
                logger.warning(
                    "❌ Thiếu UPSTASH_REDIS_REST_URL hoặc UPSTASH_REDIS_REST_TOKEN"
                )
                _redis_client = None
        except Exception as e:
            logger.error(f"Lỗi khởi tạo Redis REST client: {e}")
            _redis_client = None

    return _redis_client


def check_redis_health() -> tuple[bool, float]:
    """
    Kiểm tra sức khỏe Redis bằng cách ping server.

    Trả về:
        tuple: (is_healthy: bool, response_time: float tính bằng giây)
    """
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
