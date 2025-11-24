"""Quản lý cấu hình sử dụng Pydantic Settings."""

from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Cài đặt ứng dụng được tải từ biến môi trường."""

    # Ứng dụng
    app_name: str = "ZenSpa Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"  # development, staging, production

    # Máy chủ
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]

    # Database (Supabase PostgreSQL)
    database_url: str

    # Redis (Upstash REST API)
    upstash_redis_rest_url: str | None = None
    upstash_redis_rest_token: str | None = None

    # Logging
    log_level: str = "INFO"

    # Supabase (cho xác thực tương lai)
    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_role_key: str | None = None
    supabase_jwt_secret: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

    @property
    def cors_origins_list(self) -> List[str]:
        """Trả về origins CORS dưới dạng danh sách."""
        return self.cors_origins

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Xác thực định dạng database URL."""
        if not v.startswith("postgresql"):
            raise ValueError("DATABASE_URL phải bắt đầu bằng postgresql")
        return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def validate_cors_origins(cls, v):
        """Xác thực và parse CORS origins từ env var."""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            if not v.strip():
                return ["http://localhost:3000"]  # default
            # Handle comma-separated or single URL
            origins = [origin.strip() for origin in v.split(",") if origin.strip()]
            return origins
        return ["http://localhost:3000"]  # fallback


# Instance cài đặt toàn cục
settings = Settings()
