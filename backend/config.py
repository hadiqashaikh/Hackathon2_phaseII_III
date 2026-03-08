"""
Centralized configuration for Phase III: Todo AI Chatbot.

Uses pydantic-settings for type-safe environment variable loading.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str

    # Authentication (Better Auth)
    BETTER_AUTH_SECRET: str

    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_AGENT_MODEL: str = "gpt-4o"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"  # Default to OpenAI, can be overridden for OpenRouter
    OPENAI_MAX_TOKENS: int = 4000  # Reduced token limit for OpenRouter free tier

    # Chat Configuration
    CHATKIT_MAX_MESSAGES: int = 50

    # Server Configuration
    MCP_SERVER_PORT: int = 8000
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Frontend Configuration
    NEXT_PUBLIC_BETTER_AUTH_URL: str = "http://localhost:8000"
    NEXT_PUBLIC_API_BASE_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return "localhost" in self.DATABASE_URL or "127.0.0.1" in self.DATABASE_URL


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings
