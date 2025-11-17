from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgres://app:app@localhost:5432/appdb"
    JWT_SECRET: str = "change-me"
    JWT_ALGO: str = "HS256"
    JWT_EXPIRES_MIN: int = 480
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:8080"
    TZ: str = "UTC"
    
    class Config:
        env_file = ".env"

settings = Settings()
