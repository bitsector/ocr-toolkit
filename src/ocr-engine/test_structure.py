#!/usr/bin/env python3
"""
Test script to verify the new controller/core structure works correctly.
This can be run to validate imports and basic functionality.
"""

from util.logger import get_cli_logger

# Initialize logger for this test script
logger = get_cli_logger(__name__)


def test_imports():
    """Test that all our refactored imports work correctly"""
    logger.info("Testing imports...")

    # Test core layer imports
    try:
        from core import FileValidationService, LanguageDetectionService, OCRService

        logger.info("✅ Core layer imports successful")
    except ImportError as e:
        logger.error(f"❌ Core layer import failed: {e}")
        return False

    # Test controller layer imports
    try:
        from controllers import HealthController, OCRController

        logger.info("✅ Controllers layer imports successful")
    except ImportError as e:
        print(f"❌ Controllers layer import failed: {e}")
        return False

    # Test API layer imports
    try:
        from api.endpoints import router

        print("✅ API layer imports successful")
    except ImportError as e:
        print(f"❌ API layer import failed: {e}")
        return False

    # Test controller instantiation
    try:
        health_controller = HealthController()
        ocr_controller = OCRController()
        print("✅ Controller instantiation successful")
    except Exception as e:
        print(f"❌ Controller instantiation failed: {e}")
        return False

    # Test controller methods
    try:
        health_status = health_controller.get_root_status()
        assert "status" in health_status
        assert "message" in health_status
        print("✅ Health controller methods working")
    except Exception as e:
        print(f"❌ Health controller methods failed: {e}")
        return False

    return True


def test_structure():
    """Test the directory structure"""
    import os

    print("\nTesting directory structure...")

    # Check core directory exists
    if os.path.exists("core"):
        print("✅ core/ directory exists")
    else:
        print("❌ core/ directory missing")
        return False

    # Check controllers directory exists
    if os.path.exists("controllers"):
        print("✅ controllers/ directory exists")
    else:
        print("❌ controllers/ directory missing")
        return False

    # Check old services directory is gone
    if not os.path.exists("services"):
        print("✅ old services/ directory removed")
    else:
        print("⚠️  old services/ directory still exists")

    return True


if __name__ == "__main__":
    print("=== OCR Toolkit Structure Validation ===\n")

    imports_ok = test_imports()
    structure_ok = test_structure()

    if imports_ok and structure_ok:
        print("\n🎉 All tests passed! New structure is working correctly.")
        print("\nNew architecture:")
        print("📁 api/          → Route definitions (HTTP endpoints)")
        print("📁 controllers/  → HTTP request/response handlers")
        print("📁 core/         → Business logic and domain services")
        print("📁 models/       → Pydantic models")
        print("📁 db/           → Database layer")
        print("📁 cache/        → Caching layer")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
