"""Kết nối database và quản lý session (Async)."""

import time
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlmodel import text
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from sqlalchemy.exc import OperationalError, DBAPIError

from app.core.config import settings
from app.core.exceptions import DatabaseException
from app.core.logging import logger

# Chuyển đổi URL sang asyncpg
DATABASE_URL = settings.database_url
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Tạo engine async
engine = create_async_engine(
    DATABASE_URL,
    pool_size=settings.db_pool_size if hasattr(settings, "db_pool_size") else 10,
    max_overflow=(
        settings.db_max_overflow if hasattr(settings, "db_max_overflow") else 10
    ),
    pool_timeout=(
        settings.db_pool_timeout if hasattr(settings, "db_pool_timeout") else 30
    ),
    echo=settings.db_echo if hasattr(settings, "db_echo") else False,
    future=True,
)

# Tạo session factory với AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((OperationalError, DBAPIError)),
    reraise=True,
)
async def init_db() -> None:
    """
    Khởi tạo database với cơ chế retry (Async).
    Retry 3 lần với exponential backoff (2s, 4s, 8s).
    """
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Kết nối database thành công")
    except Exception as e:
        logger.error(f"❌ Kết nối database thất bại: {e}")
        raise DatabaseException(f"Không thể khởi tạo database: {e}")


async def close_db() -> None:
    """Đóng kết nối database."""
    await engine.dispose()
    logger.info("Kết nối database đã đóng")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency cho FastAPI.
    Cung cấp async database session, tự động close sau request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def check_database_health() -> tuple[bool, float]:
    """
    Kiểm tra sức khỏe database bằng cách thực hiện query đơn giản (Async).

    Trả về:
        tuple: (is_healthy: bool, response_time: float tính bằng giây)
    """
    start_time = time.time()
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        response_time = time.time() - start_time
        logger.debug(f"Health check database thành công trong {response_time:.3f}s")
        return True, response_time
    except Exception as e:
        response_time = time.time() - start_time
        logger.error(f"Health check database thất bại: {e}")
        return False, response_time
