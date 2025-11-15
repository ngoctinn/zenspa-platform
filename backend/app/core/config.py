"""
Application configuration using Pydantic Settings.
Loads configuration from environment variables.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="ZenSpa Backend", description="Application name")
    environment: str = Field(
        default="development",
        description="Environment (development/staging/production)",
    )
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(
        default="INFO", description="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)"
    )
    api_version: str = Field(default="v1", description="API version")

    # Database
    database_url: str = Field(..., description="PostgreSQL connection URL (async)")
    db_pool_size: int = Field(default=20, description="Database connection pool size")
    db_max_overflow: int = Field(default=5, description="Max overflow connections")
    db_pool_pre_ping: bool = Field(default=True, description="Enable pool pre-ping")
    db_echo: bool = Field(default=False, description="Echo SQL statements")

    # Redis
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database number")
    redis_password: str = Field(default="", description="Redis password")
    redis_decode_responses: bool = Field(
        default=True, description="Decode Redis responses"
    )

    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Allowed CORS origins (comma-separated)",
    )
    cors_allow_credentials: bool = Field(
        default=True, description="Allow credentials in CORS"
    )
    cors_allow_methods: str = Field(
        default="GET,POST,PUT,DELETE,PATCH,OPTIONS",
        description="Allowed HTTP methods (comma-separated)",
    )
    cors_allow_headers: str = Field(default="*", description="Allowed headers")

    # Security
    secret_key: str = Field(..., description="Secret key for security")

    # Retry configuration
    db_retry_attempts: int = Field(default=3, description="Database retry attempts")
    db_retry_wait_min: int = Field(
        default=1, description="Min wait time between retries (seconds)"
    )
    db_retry_wait_max: int = Field(
        default=10, description="Max wait time between retries (seconds)"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def cors_methods_list(self) -> list[str]:
        """Parse CORS methods from comma-separated string."""
        return [method.strip() for method in self.cors_allow_methods.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()
