"""
End-to-end tests for OCR API using sample files.
Tests the full OCR pipeline with real sample files against a running server.
"""

import os
import time
import requests
import pytest

# Configuration
SAMPLE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../sample_files")
)
OCR_URL = "http://localhost:8000/extract-text"
HEALTH_URL = "http://localhost:8000/health"

# Always use strict mode - ALL words must be found
STRICT_MODE = True

# List all sample files
sample_files = [
    f for f in os.listdir(SAMPLE_DIR) if os.path.isfile(os.path.join(SAMPLE_DIR, f))
]


def test_server_health():
    """Test that the FastAPI OCR server responds on port 8000."""
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    except Exception as e:
        assert False, f"Server health check failed: {e}"


@pytest.mark.parametrize("filename", sample_files)
def test_ocr_file_extraction(filename):
    """
    For each sample file, upload to /extract-text endpoint and check that all words
    in the filename (split by '_', lowercase, excluding extension) are present in the OCR result.
    """
    filepath = os.path.join(SAMPLE_DIR, filename)

    # Extract expected words from filename (excluding extension)
    base_name = os.path.splitext(filename)[0].lower()
    words = base_name.split("_")

    print(f"\n{'='*60}")
    print(f"TESTING FILE: {filename}")
    print(f"{'='*60}")
    print(f"Expected words: {words}")
    print(f"File path: {filepath}")

    # Send file to OCR endpoint
    with open(filepath, "rb") as f:
        # Determine content type based on file extension
        ext = os.path.splitext(filename)[1].lower()
        content_type_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".pdf": "application/pdf",
        }
        content_type = content_type_map.get(ext, "application/octet-stream")

        files = {"file": (filename, f, content_type)}
        response = requests.post(OCR_URL, files=files, timeout=30)

    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")

    # Handle response
    if response.status_code == 200:
        # Successful OCR processing
        data = response.json()
        print(f"Full response JSON: {data}")

        # Extract text from response
        assert (
            "extracted_text" in data
        ), f"Response missing 'extracted_text' field for {filename}"
        extracted_text = data["extracted_text"].lower()

        print(f"Extracted text: '{extracted_text}'")
        print(f"Extracted text length: {len(extracted_text)}")
        print(f"Confidence score: {data.get('confidence_score', 'N/A')}")

        # Check that all expected words are present in the OCR result
        missing_words = []
        for word in words:
            print(f"Looking for '{word}' in extracted text...")
            if word not in extracted_text:
                missing_words.append(word)
            else:
                print(f"✓ Found '{word}'")

        # Assert all words were found - STRICT MODE
        if missing_words:
            error_msg = (
                f"OCR FAILED: Words {missing_words} not found in OCR result for {filename}. "
                f"Expected ALL words: {words}, but got text: '{extracted_text}'"
            )
            assert False, error_msg

        print(f"{'='*60}")
        print(f"✅ COMPLETED: {filename} - ALL WORDS FOUND!")
        print(f"{'='*60}\n")

    elif response.status_code == 400:
        # Bad request - could be file format or validation issue
        data = response.json()
        print(f"Validation error response: {data}")
        assert False, f"File validation failed for {filename}: {response.text}"

    elif response.status_code == 422:
        # Unprocessable entity - OCR processing failed
        data = response.json()
        print(f"OCR processing error response: {data}")
        assert False, f"OCR processing failed for {filename}: {response.text}"

    elif response.status_code == 413:
        # File too large
        data = response.json()
        print(f"File too large response: {data}")
        assert False, f"File too large for {filename}: {response.text}"

    else:
        # Any other status codes should fail the test
        assert (
            False
        ), f"Unexpected status code {response.status_code} for {filename}: {response.text}"


def test_server_root_endpoint():
    """Test that the root endpoint responds correctly."""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "OCR Toolkit API is running"
        assert data["status"] == "healthy"
    except Exception as e:
        assert False, f"Root endpoint test failed: {e}"


if __name__ == "__main__":
    # Can be run directly for local testing
    print("Running E2E OCR tests...")
    print(f"Sample files directory: {SAMPLE_DIR}")
    print(f"Available sample files: {sample_files}")

    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
