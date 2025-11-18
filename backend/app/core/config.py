"""Application configuration with enhanced security"""

from functools import lru_cache
from typing import List

from pydantic import field_validator, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation"""

    # Application
    APP_NAME: str = "Temizlik Takip Sistemi"
    DEBUG: bool = False
    ENVIRONMENT: str = Field(default="production", pattern="^(development|staging|production)$")
    API_VERSION: str = "v1"

    # Database
    DATABASE_URL: str = Field(..., min_length=1)  # Required, no default
    DB_POOL_SIZE: int = Field(default=5, ge=1, le=20)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0, le=50)
    DB_POOL_TIMEOUT: int = Field(default=30, ge=5, le=300)
    DB_POOL_RECYCLE: int = Field(default=3600, ge=300)  # 1 hour
    DB_ECHO: bool = False  # Only enable in development

    # Security - JWT
    JWT_SECRET: str = Field(..., min_length=32)  # Required, minimum 32 chars
    JWT_ALGO: str = "HS256"
    JWT_EXPIRES_MIN: int = Field(default=15, ge=5, le=1440)  # 15 minutes (short for security)
    JWT_REFRESH_EXPIRES_DAYS: int = Field(default=7, ge=1, le=30)

    # Security - Password
    BCRYPT_ROUNDS: int = Field(default=12, ge=10, le=15)
    PASSWORD_MIN_LENGTH: int = Field(default=12, ge=8)

    # CORS
    CORS_ORIGINS: str = "http://localhost:8080,http://localhost:5173"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "GET,POST,PUT,DELETE,PATCH"
    CORS_ALLOW_HEADERS: str = "Content-Type,Authorization"

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, ge=1, le=1000)
    RATE_LIMIT_LOGIN_PER_MINUTE: int = Field(default=5, ge=1, le=20)

    # Logging
    LOG_LEVEL: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    # Redis (optional)
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False

    # Pagination
    DEFAULT_PAGE_SIZE: int = Field(default=20, ge=1, le=100)
    MAX_PAGE_SIZE: int = Field(default=100, ge=1, le=500)

    # Timezone
    TZ: str = "UTC"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        """Normalize postgres:// to postgresql://"""
        if isinstance(value, str) and value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql://", 1)
        return value

    @field_validator("JWT_SECRET")
    @classmethod
    def validate_jwt_secret(cls, value: str) -> str:
        """Validate JWT secret strength"""
        if value == "change-me" or value == "change-me-in-production":
            raise ValueError(
                "JWT_SECRET must be changed from default value. "
                "Generate a secure secret: openssl rand -hex 32"
            )
        if len(value) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters long")
        return value

    @field_validator("CORS_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, value: str) -> str:
        """Validate CORS origins"""
        if "*" in value:
            raise ValueError(
                "Wildcard CORS origins are not allowed in production. "
                "Specify exact origins."
            )
        return value

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def cors_methods_list(self) -> List[str]:
        """Get CORS methods as list"""
        return [method.strip() for method in self.CORS_ALLOW_METHODS.split(",")]

    @property
    def cors_headers_list(self) -> List[str]:
        """Get CORS headers as list"""
        return [header.strip() for header in self.CORS_ALLOW_HEADERS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance

    Returns:
        Settings instance
    """
    return Settings()


# Global settings instance
settings = get_settings()
