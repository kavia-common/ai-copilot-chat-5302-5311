"""
Configuration Management

Centralized configuration using environment variables and Pydantic settings.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables or .env file.
    """
    
    # Gemini API Configuration
    GOOGLE_GEMINI_API_KEY: str = Field(
        default="",
        description="Google Gemini API key for AI functionality"
    )
    
    MODEL_NAME: str = Field(
        default="gemini-1.5-flash",
        description="Gemini model to use for responses"
    )
    
    # Server Configuration
    HOST: str = Field(
        default="0.0.0.0",
        description="Host to bind the server to"
    )
    
    PORT: int = Field(
        default=3001,
        description="Port to run the server on"
    )
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        description="Allowed CORS origins"
    )
    
    # Logging Configuration
    LOG_LEVEL: str = Field(
        default="info",
        description="Logging level (debug, info, warning, error, critical)"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    def __init__(self, **kwargs):
        """
        Initialize settings and parse ALLOWED_ORIGINS if it's a string.
        """
        super().__init__(**kwargs)
        
        # Parse ALLOWED_ORIGINS if it's provided as a comma-separated string
        if isinstance(self.ALLOWED_ORIGINS, str):
            self.ALLOWED_ORIGINS = [
                origin.strip()
                for origin in self.ALLOWED_ORIGINS.split(",")
                if origin.strip()
            ]


# Global settings instance
settings = Settings()
