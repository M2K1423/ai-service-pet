"""Application settings"""
import os


class Settings:
    """Application configuration settings"""
    
    DEBUG = os.getenv("DEBUG", "False") == "True"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    API_KEY = os.getenv("API_KEY", "")
