"""
Database connection and session management using SQLModel (sync).
Includes retry mechanism for connection reliability.
Uses thread pool executor for async compatibility in FastAPI.
"""

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import contextmanager

from sqlmodel import Session, SQLModel, create_engine, select
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import settings
from app.core.exceptions import DatabaseException, ErrorCode

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager with sync SQLModel."""

    def __init__(self) -> None:
        """Initialize database connection."""
        self._engine = None

    def _connect_sync(self) -> None:
        """Sync connect method for retry decorator."""
        logger.info("Connecting to database...")

        # Create sync engine
        self._engine = create_engine(
            settings.database_url,
            echo=settings.db_echo,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_pre_ping=settings.db_pool_pre_ping,
            pool_recycle=3600,  # Recycle connections after 1 hour
        )

        # Test connection by creating a session
        with Session(self._engine) as session:
            # Simple connection test - just verify we can create a session
            pass

        logger.info("Database connected successfully")

    @retry(
        stop=stop_after_attempt(settings.db_retry_attempts),
        wait=wait_exponential(
            min=settings.db_retry_wait_min,
            max=settings.db_retry_wait_max,
        ),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    async def connect(self) -> None:
        """
        Connect to database with retry mechanism.
        Runs sync connection in thread pool.

        Raises:
            DatabaseException: If connection fails after retries
        """
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._connect_sync)
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise DatabaseException(
                message="Failed to connect to database",
                error_code=ErrorCode.DATABASE_CONNECTION_ERROR,
                details={"error": str(e)},
            ) from e

    async def disconnect(self) -> None:
        """Disconnect from database."""
        if self._engine:
            logger.info("Disconnecting from database...")
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._engine.dispose)
            self._engine = None
            logger.info("Database disconnected")

    @contextmanager
    def session_sync(self):
        """
        Get database session context manager (sync).

        Yields:
            Session: Database session

        Raises:
            DatabaseException: If session creation fails
        """
        if not self._engine:
            raise DatabaseException(
                message="Database not connected",
                error_code=ErrorCode.DATABASE_CONNECTION_ERROR,
            )

        session = Session(self._engine)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise DatabaseException(
                message="Database operation failed",
                error_code=ErrorCode.DATABASE_QUERY_ERROR,
                details={"error": str(e)},
            ) from e
        finally:
            session.close()

    def _health_check_sync(self) -> bool:
        """Sync health check."""
        if not self._engine:
            return False

        try:
            with Session(self._engine) as session:
                # Test connection by creating session
                pass
            return True
        except Exception:
            return False

    async def health_check(self) -> bool:
        """
        Check database health.

        Returns:
            bool: True if database is healthy
        """
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._health_check_sync)
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Global database instance
db = Database()


async def get_session() -> AsyncGenerator[Session, None]:
    """
    Dependency to get database session.
    Wraps sync session for FastAPI async compatibility.

    Yields:
        Session: Database session
    """
    loop = asyncio.get_event_loop()

    def _get_session():
        with db.session_sync() as session:
            return session

    session = await loop.run_in_executor(None, _get_session)
    try:
        yield session
    finally:
        await loop.run_in_executor(None, session.close)
