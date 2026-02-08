"""
Application settings and configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Scraping
    USER_AGENT: str = "HPCLLeadBot/1.0"
    MAX_WORKERS: int = 5
    SCRAPE_DELAY_SECONDS: int = 2
    RESPECT_ROBOTS_TXT: bool = True
    
    # AI/ML
    SPACY_MODEL: str = "en_core_web_sm"
    MIN_CONFIDENCE_THRESHOLD: float = 0.6
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Deployment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()