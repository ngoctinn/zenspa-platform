"""Main FastAPI application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import init_db, close_db
from app.redis.client import close_redis
from app.core.exceptions import (
    zenspa_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    ZenSpaException
)
from app.core.middleware import SecurityHeadersMiddleware, RequestIDMiddleware
from app.api.api_v1 import api_v1_router
from app.api.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Quản lý vòng đời ứng dụng."""
    # Khởi động
    try:
        # Thiết lập logging trước
        setup_logging()

        # Khởi tạo database
        init_db()

        app.logger.info("✅ Ứng dụng khởi động thành công")
    except Exception as e:
        app.logger.error(f"❌ Ứng dụng khởi động thất bại: {e}")
        raise

    yield

    # Tắt máy
    try:
        # Đóng kết nối database
        close_db()

        # Đóng kết nối Redis
        close_redis()

        app.logger.info("✅ Ứng dụng tắt thành công")
    except Exception as e:
        app.logger.error(f"❌ Lỗi khi tắt ứng dụng: {e}")


# Tạo ứng dụng FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API backend cho nền tảng ZenSpa",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Thêm middleware theo thứ tự đúng
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware trusted host (cho production)
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["zenspa-backend.com"]  # Cập nhật với domain thực tế
    )

# Đăng ký exception handlers
app.add_exception_handler(ZenSpaException, zenspa_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Bao gồm routers
app.include_router(api_v1_router)

# Health checks (toàn cục, không versioned)
app.include_router(
    health_router,
    prefix="/health",
    tags=["health"]
)


@app.get("/")
async def root():
    """Endpoint gốc."""
    return {
        "message": "Chào mừng đến với ZenSpa Backend API",
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs",
        "health": "/health"
    }


# Health check cho root path (thay thế)
@app.get("/ping")
async def ping():
    """Endpoint ping đơn giản."""
    return {"status": "pong"}
