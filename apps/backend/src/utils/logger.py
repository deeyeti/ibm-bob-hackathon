"""
Logging configuration for Eco-Shift backend.
"""

import logging
import sys
from typing import Optional
from pythonjsonlogger import jsonlogger

from src.config import settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging."""

    def add_fields(self, log_record, record, message_dict):
        """Add custom fields to log records."""
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        # Add custom fields
        log_record["app_name"] = settings.app_name
        log_record["environment"] = settings.environment
        log_record["level"] = record.levelname
        log_record["logger_name"] = record.name


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or __name__)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set log level from settings
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Use JSON formatter in production, simple formatter in development
    if settings.is_production:
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(level)s %(name)s %(message)s",
            rename_fields={"levelname": "level", "name": "logger_name"},
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def setup_logging() -> None:
    """
    Setup application-wide logging configuration.
    Should be called once at application startup.
    """
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    if settings.is_production:
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(level)s %(name)s %(message)s"
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


# Initialize logging on module import
setup_logging()

# Made with Bob
