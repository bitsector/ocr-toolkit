import time
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import models from the models package
from models import (
    DetectedLanguage,
    DetectLanguageResponse,
    ErrorResponse,
    ExtractTextResponse,
)

# Import services
from services import LanguageDetectionService, OCRService

# Create API router
router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint - API health check"""
    return {"message": "OCR Toolkit API is running", "status": "healthy"}


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}


@router.post(
    "/extract-text",
    response_model=ExtractTextResponse,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Bad request - invalid file format or missing file",
        },
        413: {"model": ErrorResponse, "description": "File too large"},
        422: {
            "model": ErrorResponse,
            "description": "Unprocessable entity - file cannot be processed",
        },
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Extract text from image or document",
    description="Uploads a file and extracts all readable text from it using OCR technology. Supports JPEG, PNG, WEBP, and PDF formats.",
    tags=["OCR Operations"],
)
async def extract_text(
    file: UploadFile = File(
        ..., description="Image or document file (supports JPEG, PNG, WEBP, PDF)"
    )
) -> ExtractTextResponse:
    """
    Extract text from an uploaded image or document file.

    This endpoint processes the uploaded file and returns the extracted text along with
    confidence scores and processing time metrics.
    """
    try:
        # Use OCR service to extract text
        (
            extracted_text,
            confidence_score,
            processing_time,
        ) = await OCRService.extract_text(file)

        return ExtractTextResponse(
            success=True,
            extracted_text=extracted_text,
            confidence_score=confidence_score,
            processing_time=processing_time,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post(
    "/detect-language",
    response_model=DetectLanguageResponse,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Bad request - invalid file format or missing file",
        },
        413: {"model": ErrorResponse, "description": "File too large"},
        422: {
            "model": ErrorResponse,
            "description": "Unprocessable entity - file cannot be processed",
        },
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Detect languages in image or document",
    description="Uploads a file and detects the languages used in the text content. Returns detected languages with confidence scores.",
    tags=["OCR Operations"],
)
async def detect_language(
    file: UploadFile = File(
        ..., description="Image or document file (supports JPEG, PNG, WEBP, PDF)"
    )
) -> DetectLanguageResponse:
    """
    Detect languages in an uploaded image or document file.

    This endpoint processes the uploaded file, extracts text, and identifies the languages
    present in the content along with confidence scores and percentages.
    """
    try:
        # Use language detection service
        (
            detected_languages_data,
            primary_language,
            processing_time,
        ) = await LanguageDetectionService.detect_language_in_file(file)

        # Convert to Pydantic models
        detected_languages = [
            DetectedLanguage(
                language=lang_data["language"],
                language_code=lang_data["language_code"],
                confidence=lang_data["confidence"],
                text_percentage=lang_data["text_percentage"],
            )
            for lang_data in detected_languages_data
        ]

        return DetectLanguageResponse(
            success=True,
            detected_languages=detected_languages,
            primary_language=primary_language,
            processing_time=processing_time,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Add a new request body model for text-based language detection
class TextRequest(BaseModel):
    text: str = Field(..., description="Text to analyze for language detection")


@router.post(
    "/detect-language-text",
    response_model=DetectLanguageResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request - no text provided"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Detect languages in text",
    description="Analyze provided text and detect the languages used. Returns detected languages with confidence scores.",
    tags=["OCR Operations"],
)
async def detect_language_text(request: TextRequest) -> DetectLanguageResponse:
    """
    Detect languages in provided text.

    This endpoint analyzes the provided text and identifies the languages
    present in the content along with confidence scores and percentages.
    """
    try:
        start_time = time.time()

        # Use language detection service directly on text
        detected_languages_data = LanguageDetectionService.detect_languages(
            request.text
        )

        # Determine primary language
        primary_language = (
            detected_languages_data[0]["language"]
            if detected_languages_data
            else "Unknown"
        )

        # Convert to Pydantic models
        detected_languages = [
            DetectedLanguage(
                language=lang_data["language"],
                language_code=lang_data["language_code"],
                confidence=lang_data["confidence"],
                text_percentage=lang_data["text_percentage"],
            )
            for lang_data in detected_languages_data
        ]

        processing_time = time.time() - start_time

        return DetectLanguageResponse(
            success=True,
            detected_languages=detected_languages,
            primary_language=primary_language,
            processing_time=processing_time,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
