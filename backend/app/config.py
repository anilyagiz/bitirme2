from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://app:app@localhost:5432/appdb"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # JWT
    JWT_SECRET: str = "change-me"
    JWT_ALGO: str = "HS256"
    JWT_EXPIRES_MIN: int = 480

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:8080"

    # App Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "info"
    TZ: str = "UTC"

    # Security
    RATE_LIMIT_ENABLED: bool = False
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Validate critical settings in production
if settings.ENVIRONMENT == "production":
    if settings.JWT_SECRET == "change-me":
        raise ValueError("JWT_SECRET must be changed in production!")
    if settings.DEBUG:
        raise ValueError("DEBUG must be False in production!")
