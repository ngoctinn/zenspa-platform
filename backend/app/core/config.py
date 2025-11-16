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

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None
    redis_decode_responses: bool = True

    # Logging
    log_level: str = "INFO"

    # Supabase (cho xác thực tương lai)
    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_role_key: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        """Trả về origins CORS dưới dạng danh sách."""
        return self.cors_origins

    @field_validator('database_url')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Xác thực định dạng database URL."""
        if not v.startswith('postgresql'):
            raise ValueError('DATABASE_URL phải bắt đầu bằng postgresql')
        return v


# Instance cài đặt toàn cục
settings = Settings()
