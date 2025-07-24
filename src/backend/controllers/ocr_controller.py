# OCR Controller - HTTP request/response handlers for OCR operations
# This layer handles HTTP-specific concerns like request validation, response formatting,
# error handling, and delegates business logic to the core layer.

from typing import Any, Dict, List

from fastapi import HTTPException, UploadFile

from models import DetectedLanguage, DetectLanguageResponse, ExtractTextResponse


class OCRController:
    """
    Controller for OCR-related HTTP endpoints.
    Handles HTTP concerns like request validation, error formatting, and response formatting.
    This controller is synchronous - it only processes HTTP requests/responses.
    Business logic is delegated to the core layer, which is called asynchronously by endpoints.
    """

    def validate_extract_text_request(self, file: UploadFile) -> None:
        """
        Validate text extraction request parameters.
        Synchronous validation of HTTP request before processing.
        """
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        if not file.filename:
            raise HTTPException(status_code=400, detail="File must have a filename")

    def format_extract_text_response(
        self, extracted_text: str, confidence_score: float, processing_time: float
    ) -> ExtractTextResponse:
        """
        Format the OCR results into HTTP response.
        Synchronous response formatting after business logic completion.
        """
        return ExtractTextResponse(
            success=True,
            extracted_text=extracted_text,
            confidence_score=confidence_score,
            processing_time=processing_time,
        )

    def validate_detect_language_request(self, file: UploadFile) -> None:
        """
        Validate language detection request parameters.
        Synchronous validation of HTTP request before processing.
        """
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        if not file.filename:
            raise HTTPException(status_code=400, detail="File must have a filename")

    def format_detect_language_response(
        self,
        detected_languages_data: List[Dict[str, Any]],
        primary_language: str,
        processing_time: float,
    ) -> DetectLanguageResponse:
        """
        Format the language detection results into HTTP response.
        Synchronous response formatting after business logic completion.
        """
        # Convert to Pydantic models for HTTP response
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

    def handle_service_error(self, error: Exception) -> HTTPException:
        """
        Convert service layer errors to appropriate HTTP exceptions.
        Synchronous error handling and formatting.
        """
        if isinstance(error, HTTPException):
            return error
        return HTTPException(
            status_code=500, detail=f"Internal server error: {str(error)}"
        )
