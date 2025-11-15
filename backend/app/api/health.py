"""
Health check endpoints.
"""

import logging

from fastapi import APIRouter, status

from app.common.schemas import HealthResponse
from app.core.config import settings
from app.core.database import db
from app.redis.client import redis_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Overall health check",
    description="Check the overall health of the application including database and Redis",
)
async def health_check() -> HealthResponse:
    """
    Overall health check endpoint.

    Returns health status of the application with database and Redis status.
    """
    # Check database
    db_healthy = await db.health_check()

    # Check Redis
    redis_healthy = await redis_client.health_check()

    # Determine overall status
    overall_status = "healthy" if db_healthy else "unhealthy"

    return HealthResponse(
        status=overall_status,
        service=settings.app_name,
        version=settings.api_version,
        details={
            "database": "healthy" if db_healthy else "unhealthy",
            "redis": "healthy" if redis_healthy else "unavailable",
            "environment": settings.environment,
        },
    )


@router.get(
    "/db",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Database health check",
    description="Check database connection health",
)
async def database_health_check() -> HealthResponse:
    """
    Database health check endpoint.

    Returns health status of the database connection.
    """
    db_healthy = await db.health_check()

    return HealthResponse(
        status="healthy" if db_healthy else "unhealthy",
        service="Database",
        version=settings.api_version,
        details={
            "connection": "active" if db_healthy else "failed",
        },
    )


@router.get(
    "/redis",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Redis health check",
    description="Check Redis connection health",
)
async def redis_health_check() -> HealthResponse:
    """
    Redis health check endpoint.

    Returns health status of the Redis connection.
    """
    redis_healthy = await redis_client.health_check()

    return HealthResponse(
        status="healthy" if redis_healthy else "unavailable",
        service="Redis",
        version=settings.api_version,
        details={
            "connection": "active" if redis_healthy else "unavailable",
            "available": redis_client.is_available,
        },
    )
