# Utility function to get a config value from environment, .env, or default
def get_config_value(key: str, default: str = None) -> str:
    """
    Get a configuration value from environment variables, .env, or default.
    Args:
        key (str): The environment variable/config key
        default (str, optional): The default value if not set. Defaults to None.
    Returns:
        str: The value as a string (or default if not set)
    """
    # Priority: environment variable > .env > default
    value = os.getenv(key)
    if value is not None:
        return value
    # Optionally, you could load from .env here if needed, but os.getenv covers both if dotenv is loaded
    return default


"""
Configuration management for OCR Toolkit

This module provides centralized configuration management with the following priority:
1. Environment variables (highest priority)
2. .env file values
3. Hardcoded defaults (lowest priority)

Usage:
    from util.config import get_config

    config = get_config()
    max_file_size = config.max_file_size
    ocr_confidence = config.ocr_confidence_score
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

from util.logger import get_service_logger

logger = get_service_logger(__name__)


@dataclass
class OCRConfig:
    """Configuration data class for OCR Toolkit"""

    # File processing limits
    max_file_size: int  # Maximum file size in bytes

    # OCR confidence scores
    ocr_confidence_score: float  # Confidence score when OCR finds text
    ocr_no_text_confidence: float  # Confidence score when no text is found
    pdf_text_confidence: float  # Confidence score for direct PDF text extraction
    language_detection_fallback_confidence: float  # Fallback confidence for language detection

    # Content type configuration
    allowed_content_types: List[str]  # List of allowed MIME types

    # Language detection
    fallback_language: str  # Default language when detection fails
    fallback_language_code: str  # Default language code when detection fails


def _get_env_str(key: str, default: str) -> str:
    """Get environment variable as string"""
    return os.getenv(key, default)


def _get_env_int(key: str, default: int) -> int:
    """Get environment variable as int"""
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to convert {key}='{value}' to int: {e}")
        return default


def _get_env_float(key: str, default: float) -> float:
    """Get environment variable as float"""
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to convert {key}='{value}' to float: {e}")
        return default


def _get_env_var(
    key: str, default: Union[str, int, float, bool, List[str]], var_type: type = str
) -> Union[str, int, float, bool, List[str]]:
    """
    Get environment variable with type conversion and default fallback

    Args:
        key: Environment variable name
        default: Default value if not found
        var_type: Type to convert the value to

    Returns:
        The environment variable value converted to the specified type, or default
    """
    value = os.getenv(key)

    if value is None:
        return default

    try:
        if var_type == bool:
            return value.lower() in ("true", "1", "yes", "on")
        elif var_type == int:
            return int(value)
        elif var_type == float:
            return float(value)
        elif var_type == list:
            # For lists, expect comma-separated values
            return [item.strip() for item in value.split(",") if item.strip()]
        else:
            return value
    except (ValueError, TypeError) as e:
        logger.warning(
            f"Failed to convert environment variable {key}='{value}' to {var_type.__name__}: {e}"
        )
        return default


def _load_env_file() -> None:
    """
    Load environment variables from .env file in project root
    Only loads if variables are not already set in environment
    """
    # Find project root (where .env should be located)
    current_dir = Path(__file__).resolve()
    project_root = None

    # Look for .env file by going up directories until we find it or reach root
    for parent in current_dir.parents:
        env_file = parent / ".env"
        if env_file.exists():
            project_root = parent
            break

    if project_root is None:
        logger.debug("No .env file found in project hierarchy")
        return

    env_file = project_root / ".env"

    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Parse KEY=VALUE format
                if "=" not in line:
                    logger.warning(
                        f"Invalid .env format in {env_file}:{line_num}: {line}"
                    )
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]

                # Only set if not already in environment
                if key not in os.environ:
                    os.environ[key] = value
                    logger.debug(f"Loaded {key} from .env file")
                else:
                    logger.debug(
                        f"Environment variable {key} already set, skipping .env value"
                    )

    except Exception as e:
        logger.warning(f"Failed to load .env file {env_file}: {e}")


def get_config() -> OCRConfig:
    """
    Get the complete OCR configuration

    Returns:
        OCRConfig: Configuration object with all settings
    """
    # Load .env file first (only if env vars not already set)
    _load_env_file()

    logger.debug(
        "Loading OCR configuration from environment variables, .env file, and defaults"
    )

    # File processing limits
    max_file_size = _get_env_int("OCR_MAX_FILE_SIZE", 10 * 1024 * 1024)  # 10MB default

    # OCR confidence scores
    ocr_confidence_score = _get_env_float("OCR_CONFIDENCE_SCORE", 0.85)
    ocr_no_text_confidence = _get_env_float("OCR_NO_TEXT_CONFIDENCE", 0.0)
    pdf_text_confidence = _get_env_float("PDF_TEXT_CONFIDENCE", 0.95)
    language_detection_fallback_confidence = _get_env_float(
        "LANGUAGE_DETECTION_FALLBACK_CONFIDENCE", 0.5
    )

    # Content types (comma-separated in env var)
    default_content_types = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/webp",
        "application/pdf",
    ]
    # For list types, we need to handle the conversion differently
    allowed_content_types_env = os.getenv("OCR_ALLOWED_CONTENT_TYPES")
    if allowed_content_types_env:
        allowed_content_types = [
            item.strip()
            for item in allowed_content_types_env.split(",")
            if item.strip()
        ]
    else:
        allowed_content_types = default_content_types

    # Language detection fallbacks
    fallback_language = _get_env_str("LANGUAGE_DETECTION_FALLBACK_LANGUAGE", "English")
    fallback_language_code = _get_env_str("LANGUAGE_DETECTION_FALLBACK_CODE", "en")

    config = OCRConfig(
        max_file_size=max_file_size,
        ocr_confidence_score=ocr_confidence_score,
        ocr_no_text_confidence=ocr_no_text_confidence,
        pdf_text_confidence=pdf_text_confidence,
        language_detection_fallback_confidence=language_detection_fallback_confidence,
        allowed_content_types=allowed_content_types,
        fallback_language=fallback_language,
        fallback_language_code=fallback_language_code,
    )

    logger.info(
        f"Configuration loaded - Max file size: {config.max_file_size} bytes, OCR confidence: {config.ocr_confidence_score}"
    )

    return config


# Global configuration instance (loaded once on import)
_config_instance = None


def get_cached_config() -> OCRConfig:
    """
    Get cached configuration instance (loads once, reuses afterwards)

    Returns:
        OCRConfig: Cached configuration object
    """
    global _config_instance

    if _config_instance is None:
        _config_instance = get_config()
        logger.debug("Configuration cached for reuse")

    return _config_instance


def reload_config() -> OCRConfig:
    """
    Force reload configuration from environment/files

    Returns:
        OCRConfig: Newly loaded configuration object
    """
    global _config_instance

    logger.info("Reloading configuration...")
    _config_instance = get_config()

    return _config_instance
