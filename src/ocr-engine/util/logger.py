"""
Professional logging configuration for OCR Toolkit.

This module provides a centralized logging configuration following Python best practices.
It supports structured logging with appropriate levels, formatting, and output handling.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def get_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_style: str = "detailed",
) -> logging.Logger:
    """
    Get a configured logger instance with professional formatting.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output (None for console only)
        format_style: Format style ("detailed", "simple", "json")
    
    Returns:
        Configured logger instance
    
    Example:
        >>> from util.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
        >>> logger.debug("Debug information", extra={"user_id": 123})
        >>> logger.error("An error occurred", exc_info=True)
    """
    
    # Create logger
    logger = logging.getLogger(name)
    
    # Prevent duplicate handlers if logger already configured
    if logger.handlers:
        return logger
    
    # Set level
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatters
    formatters = {
        "detailed": logging.Formatter(
            fmt="%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ),
        "simple": logging.Formatter(
            fmt="%(levelname)s: %(message)s"
        ),
        "json": logging.Formatter(
            fmt='{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", '
                '"function": "%(funcName)s", "line": %(lineno)d, "message": "%(message)s"}',
            datefmt="%Y-%m-%dT%H:%M:%S"
        )
    }
    
    formatter = formatters.get(format_style, formatters["detailed"])
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to parent loggers to avoid duplicate messages
    logger.propagate = False
    
    return logger


def setup_application_logging(
    app_name: str = "ocr-toolkit",
    level: str = "INFO",
    log_dir: Optional[str] = None,
) -> logging.Logger:
    """
    Setup application-wide logging configuration.
    
    Args:
        app_name: Application name for the root logger
        level: Default logging level
        log_dir: Directory for log files (None for console only)
    
    Returns:
        Root application logger
    """
    
    log_file = None
    if log_dir:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        log_file = str(log_path / f"{app_name}.log")
    
    return get_logger(app_name, level=level, log_file=log_file)


def get_cli_logger(name: str, verbose: bool = False) -> logging.Logger:
    """
    Get a logger optimized for CLI applications with user-friendly output.
    
    Args:
        name: Logger name
        verbose: If True, use detailed formatting; if False, use simple formatting
    
    Returns:
        CLI-optimized logger
    """
    
    level = "DEBUG" if verbose else "INFO"
    format_style = "detailed" if verbose else "simple"
    
    return get_logger(name, level=level, format_style=format_style)


# Pre-configured loggers for common use cases
def get_api_logger(name: str) -> logging.Logger:
    """Get a logger configured for API components."""
    return get_logger(name, level="INFO", format_style="detailed")


def get_service_logger(name: str) -> logging.Logger:
    """Get a logger configured for service/business logic components."""
    return get_logger(name, level="INFO", format_style="detailed")


def get_debug_logger(name: str) -> logging.Logger:
    """Get a logger configured for debugging with verbose output."""
    return get_logger(name, level="DEBUG", format_style="detailed")
