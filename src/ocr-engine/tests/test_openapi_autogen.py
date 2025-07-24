"""
Tests for OpenAPI documentation generation and accessibility.
"""

import pytest
from fastapi.testclient import TestClient

from fast_api_server import app

client = TestClient(app)


def test_openapi_docs_accessible():
    """Test that OpenAPI docs are accessible via Swagger UI."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_docs_accessible():
    """Test that OpenAPI docs are accessible via ReDoc."""
    response = client.get("/redoc")
    assert response.status_code == 200


def test_openapi_json_endpoint():
    """Test that OpenAPI JSON schema is accessible and valid."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data


def test_openapi_schema_structure():
    """Test that OpenAPI schema contains expected endpoints and structure."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()

    # Check basic OpenAPI structure
    assert data["openapi"].startswith("3.")
    assert "title" in data["info"]
    assert "version" in data["info"]

    # Check that our main endpoints are documented
    paths = data["paths"]
    assert "/" in paths
    assert "/health" in paths
    assert "/extract-text" in paths
    assert "/detect-language" in paths

    # Check that endpoints have proper HTTP methods
    assert "get" in paths["/"]
    assert "get" in paths["/health"]
    assert "post" in paths["/extract-text"]
    assert "post" in paths["/detect-language"]


def test_openapi_endpoint_details():
    """Test that OpenAPI schema contains proper endpoint details."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()

    # Check extract-text endpoint details
    extract_text = data["paths"]["/extract-text"]["post"]
    assert "summary" in extract_text
    assert "description" in extract_text
    assert "tags" in extract_text
    assert "OCR Operations" in extract_text["tags"]

    # Check detect-language endpoint details
    detect_language = data["paths"]["/detect-language"]["post"]
    assert "summary" in detect_language
    assert "description" in detect_language
    assert "tags" in detect_language
    assert "OCR Operations" in detect_language["tags"]


def test_openapi_response_models():
    """Test that OpenAPI schema includes proper response models."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()

    # Check that components/schemas section exists
    assert "components" in data
    assert "schemas" in data["components"]

    schemas = data["components"]["schemas"]

    # Check for our main response models
    assert "ExtractTextResponse" in schemas
    assert "DetectLanguageResponse" in schemas
    assert "ErrorResponse" in schemas
    assert "DetectedLanguage" in schemas
