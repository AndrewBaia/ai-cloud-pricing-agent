"""
Logging configuration for the AI Agent system.
"""
import os
import sys
from pathlib import Path
from loguru import logger

from .config import Config


def setup_logging():
    """Configure logging for the application."""

    # Create logs directory if it doesn't exist
    log_dir = Path(Config.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Remove default logger
    logger.remove()

    # Add console logger with appropriate level
    log_level = Config.LOG_LEVEL.upper()
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    # Add file logger
    logger.add(
        Config.LOG_FILE,
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="1 week",
        encoding="utf-8"
    )

    logger.info("Logging configured successfully")
    logger.info(f"Log level: {log_level}")
    logger.info(f"Log file: {Config.LOG_FILE}")


def get_logger(name: str):
    """Get a logger instance with the specified name."""
    return logger.bind(name=name)
