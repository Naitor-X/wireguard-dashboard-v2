from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "WireGuard Dashboard"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS-Konfiguration
    CORS_ORIGINS: List[str] = ["http://frontend:3000"]
    
    # JWT-Konfiguration
    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"  # In Produktion ändern!
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Datenbank-Konfiguration
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/wireguard"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 