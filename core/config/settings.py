"""Application settings."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # App settings
    APP_NAME: str = "AI Communication Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API settings
    API_KEYS: str = ""
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    
   
    
    # AI Model settings
    GOOGLE_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Default AI model
    DEFAULT_AI_MODEL: str = "gemini"  # gemini, openai, claude
    
    # Memory settings
    MAX_CONVERSATION_HISTORY: int = 50
    SESSION_TIMEOUT_MINUTES: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get settings instance (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# For backward compatibility
settings = get_settings()
