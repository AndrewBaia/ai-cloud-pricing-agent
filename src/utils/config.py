"""
Configuration management for the AI Agent system.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application."""

    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

    # Model Configuration
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4")
    DEFAULT_EMBEDDING_MODEL: str = os.getenv("DEFAULT_EMBEDDING_MODEL", "text-embedding-ada-002")

    # ChromaDB Configuration
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./data/chromadb")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/agent.log")

    # External API Configuration
    EXTERNAL_API_BASE_URL: str = os.getenv("EXTERNAL_API_BASE_URL", "http://localhost:8001")
    EXTERNAL_API_KEY: str = os.getenv("EXTERNAL_API_KEY", "demo_key")

    # Application Settings
    APP_NAME: str = "AI Cloud Pricing Agent"
    APP_VERSION: str = "1.0.0"

    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present."""
        required_vars = []

        # At least one API key should be present
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            required_vars.append("OPENAI_API_KEY or ANTHROPIC_API_KEY")

        if required_vars:
            print(f"Missing required environment variables: {', '.join(required_vars)}")
            print("Please set them in your .env file or environment.")
            return False

        return True

    @classmethod
    def get_available_models(cls) -> list[str]:
        """Get list of available models based on API keys."""
        models = []

        if cls.OPENAI_API_KEY:
            models.extend(["gpt-4", "gpt-3.5-turbo"])

        if cls.ANTHROPIC_API_KEY:
            models.extend(["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"])

        return models

    @classmethod
    def print_config(cls):
        """Print current configuration (without sensitive data)."""
        print(f"App Name: {cls.APP_NAME}")
        print(f"Version: {cls.APP_VERSION}")
        print(f"Default Model: {cls.DEFAULT_MODEL}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"ChromaDB Path: {cls.CHROMA_DB_PATH}")
        print(f"External API URL: {cls.EXTERNAL_API_BASE_URL}")
        print(f"OpenAI Key Set: {'Yes' if cls.OPENAI_API_KEY else 'No'}")
        print(f"Anthropic Key Set: {'Yes' if cls.ANTHROPIC_API_KEY else 'No'}")
        print(f"Available Models: {cls.get_available_models()}")
