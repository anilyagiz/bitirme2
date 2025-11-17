from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgres://app:app@db:5432/appdb"
    JWT_SECRET: str = "change-me"
    JWT_ALGO: str = "HS256"
    JWT_EXPIRES_MIN: int = 480
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:8080"
    TZ: str = "UTC"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if isinstance(value, str) and value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql://", 1)
        return value

    class Config:
        env_file = ".env"

settings = Settings()
