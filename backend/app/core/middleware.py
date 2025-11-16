"""Middleware cho ứng dụng FastAPI."""

import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Thêm security headers cho tất cả responses."""

    HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "X-Permitted-Cross-Domain-Policies": "none",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    async def dispatch(self, request: Request, call_next):
        """Thêm security headers vào response."""
        response = await call_next(request)
        for header, value in self.HEADERS.items():
            response.headers[header] = value
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Tạo và track request ID để logging và tracing."""

    async def dispatch(self, request: Request, call_next):
        """Tạo request ID và thêm vào request state và response headers."""
        # Lấy hoặc tạo request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Lưu vào request state để logging
        request.state.request_id = request_id

        # Xử lý request
        response = await call_next(request)

        # Thêm vào response header
        response.headers["X-Request-ID"] = request_id

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log thông tin request/response."""

    async def dispatch(self, request: Request, call_next):
        """Log chi tiết request và status response."""
        import time

        start_time = time.time()
        request_id = getattr(request.state, 'request_id', 'unknown')

        # Log request
        logger.info(f"Request: {request.method} {request.url.path}", extra={
            'request_id': request_id,
            'method': request.method,
            'path': request.url.path,
            'query': str(request.url.query),
            'user_agent': request.headers.get('user-agent', ''),
        })

        # Xử lý request
        response = await call_next(request)

        # Tính thời gian
        duration = time.time() - start_time

        # Log response
        logger.info(f"Response: {response.status_code} trong {duration:.3f}s", extra={
            'request_id': request_id,
            'status_code': response.status_code,
            'duration': duration,
        })

        return response
