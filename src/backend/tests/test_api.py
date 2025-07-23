"""
Basic tests for the OCR Toolkit API.
"""

import pytest
from fastapi.testclient import TestClient

from fast_api_server import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "OCR Toolkit API is running"
    assert data["status"] == "healthy"


def test_extract_text_endpoint_no_file():
    """Test extract text endpoint without file."""
    response = client.post("/extract-text")
    assert response.status_code == 422  # Validation error


def test_detect_language_endpoint_no_text():
    """Test detect language endpoint without text."""
    response = client.post("/detect-language")
    assert response.status_code == 422  # Validation error


def test_detect_language_endpoint_with_text():
    """Test detect language endpoint with JSON text - should fail since it only accepts files."""
    # Try to send JSON text instead of a file - this should fail
    response = client.post(
        "/detect-language",
        json={"text": "Hello world, this is a test in English."},
    )
    # Should fail because the endpoint only accepts file uploads, not JSON text
    assert response.status_code == 422  # Validation error - no file provided
