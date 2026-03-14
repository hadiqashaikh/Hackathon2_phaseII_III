"""
Configuration for Todo AI Chatbot Backend.
Uses pydantic-settings for type-safe environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # Database
    DATABASE_URL: str

    # Authentication
    BETTER_AUTH_SECRET: str

    # OpenRouter (FREE tier)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_AGENT_MODEL: str = "google/gemini-2.0-flash-lite-001"

    # OpenAI (fallback)
    OPENAI_API_KEY: str = ""
    OPENAI_MAX_TOKENS: int = 2000

    # Server
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Debug mode
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
