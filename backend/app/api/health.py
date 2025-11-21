"""Health check endpoints."""

from datetime import datetime
from fastapi import APIRouter, status
from app.common.schemas import (
    HealthCheckResponse,
    DatabaseHealthResponse,
    RedisHealthResponse,
)
from app.core.config import settings
from app.core.database import check_database_health
from app.redis.client import check_redis_health
from app.core.logging import logger

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check Tổng Quan",
    description="Kiểm tra sức khỏe tổng quan của ứng dụng",
)
async def health_check() -> HealthCheckResponse:
    """Health check endpoint tổng quan."""
    logger.info("Health check endpoint được gọi")
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        service=settings.app_name,
        version=settings.app_version,
    )


@router.get(
    "/health/db",
    response_model=DatabaseHealthResponse,
    summary="Health Check Database",
    description="Kiểm tra kết nối PostgreSQL và thời gian phản hồi",
)
async def database_health_check() -> DatabaseHealthResponse:
    """Health check endpoint cho database."""
    is_healthy, response_time = await check_database_health()

    return DatabaseHealthResponse(
        status="healthy" if is_healthy else "unhealthy",
        timestamp=datetime.utcnow(),
        service=settings.app_name,
        version=settings.app_version,
        database="postgresql",
        connected=is_healthy,
        response_time_ms=round(response_time * 1000, 2),  # Chuyển sang milliseconds
    )


@router.get(
    "/health/redis",
    response_model=RedisHealthResponse,
    summary="Health Check Redis",
    description="Kiểm tra kết nối Redis và thời gian phản hồi",
)
async def redis_health_check() -> RedisHealthResponse:
    """Health check endpoint cho Redis."""
    is_healthy, response_time = check_redis_health()

    redis_url = settings.upstash_redis_rest_url or "Not configured"

    return RedisHealthResponse(
        status="healthy" if is_healthy else "unhealthy",
        timestamp=datetime.utcnow(),
        service=settings.app_name,
        version=settings.app_version,
        redis=redis_url,
        connected=is_healthy,
        response_time_ms=round(response_time * 1000, 2),  # Chuyển sang milliseconds
    )


@router.get(
    "/health/all",
    summary="Health Check Toàn Diện",
    description="Kiểm tra tất cả services (database, redis) và trả về trạng thái tổng quan",
)
async def comprehensive_health_check():
    """Health check toàn diện cho tất cả services."""
    # Kiểm tra database
    db_healthy, db_time = await check_database_health()

    # Kiểm tra Redis
    redis_healthy, redis_time = check_redis_health()

    # Trạng thái tổng quan
    overall_healthy = db_healthy and redis_healthy

    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.app_name,
        "version": settings.app_version,
        "checks": {
            "database": {
                "healthy": db_healthy,
                "response_time_ms": round(db_time * 1000, 2),
            },
            "redis": {
                "healthy": redis_healthy,
                "response_time_ms": round(redis_time * 1000, 2),
            },
        },
    }
