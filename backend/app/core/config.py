from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "National Weather Analytics Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "dev-secret-change-in-production"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    OPEN_METEO_FORECAST_URL: str = "https://api.open-meteo.com/v1/forecast"
    OPEN_METEO_HISTORICAL_URL: str = "https://archive-api.open-meteo.com/v1/archive"
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/weather.db"
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    MODEL_DIR: str = "./models"
    DATA_DIR: str = "./data"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
