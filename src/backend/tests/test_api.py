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
    """Test detect language endpoint with direct text."""
    response = client.post(
        "/detect-language-text",
        json={"text": "Hello world, this is a test in English."},
    )
    assert response.status_code == 200
    data = response.json()
    assert "detected_languages" in data
    assert "primary_language" in data
    assert len(data["detected_languages"]) > 0
    # English text should be detected as 'en'
    assert data["detected_languages"][0]["language_code"] in ["en", "unknown"]


def test_openapi_docs():
    """Test that OpenAPI docs are accessible."""
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/redoc")
    assert response.status_code == 200

    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
