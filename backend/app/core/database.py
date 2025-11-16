"""Kết nối database và quản lý session."""

import time
from contextlib import contextmanager
from typing import Generator
from sqlmodel import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
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


# Tạo engine sync
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=settings.db_pool_size if hasattr(settings, "db_pool_size") else 10,
    max_overflow=(
        settings.db_max_overflow if hasattr(settings, "db_max_overflow") else 10
    ),
    pool_timeout=(
        settings.db_pool_timeout if hasattr(settings, "db_pool_timeout") else 30
    ),
    echo=settings.db_echo if hasattr(settings, "db_echo") else False,
)

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((OperationalError, DBAPIError)),
    reraise=True,
)
def init_db() -> None:
    """
    Khởi tạo database với cơ chế retry.
    Retry 3 lần với exponential backoff (2s, 4s, 8s).
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()
        logger.info("✅ Kết nối database thành công")
    except Exception as e:
        logger.error(f"❌ Kết nối database thất bại: {e}")
        raise DatabaseException(f"Không thể khởi tạo database: {e}")


def close_db() -> None:
    """Đóng kết nối database."""
    engine.dispose()
    logger.info("Kết nối database đã đóng")


def get_db() -> Generator[Session, None, None]:
    """
    Dependency cho FastAPI.
    Cung cấp database session, tự động close sau request.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def check_database_health() -> tuple[bool, float]:
    """
    Kiểm tra sức khỏe database bằng cách thực hiện query đơn giản.

    Trả về:
        tuple: (is_healthy: bool, response_time: float tính bằng giây)
    """
    start_time = time.time()
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()
        response_time = time.time() - start_time
        logger.debug(f"Health check database thành công trong {response_time:.3f}s")
        return True, response_time
    except Exception as e:
        response_time = time.time() - start_time
        logger.error(f"Health check database thất bại: {e}")
        return False, response_time
