from fastapi import APIRouter, File, HTTPException, UploadFile

from controllers.health_controller import HealthController

# Import controllers for HTTP handling
from controllers.ocr_controller import OCRController

# Import core services for business logic
from core import LanguageDetectionService, OCRService

# Import models from the models package
from models import DetectLanguageResponse, ErrorResponse, ExtractTextResponse

# Create API router
router = APIRouter()

# Initialize controllers
ocr_controller = OCRController()
health_controller = HealthController()


@router.get("/")
async def root():
    """Root endpoint - API health check"""
    return health_controller.get_root_status()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return health_controller.get_health_status()


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
        # Controller handles HTTP validation (synchronous)
        ocr_controller.validate_extract_text_request(file)

        # Core service handles business logic (asynchronous)
        (
            extracted_text,
            confidence_score,
            processing_time,
        ) = await OCRService.extract_text(file)

        # Controller handles response formatting (synchronous)
        return ocr_controller.format_extract_text_response(
            extracted_text, confidence_score, processing_time
        )

    except HTTPException:
        raise
    except Exception as e:
        # Controller handles error formatting (synchronous)
        raise ocr_controller.handle_service_error(e)


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
        # Controller handles HTTP validation (synchronous)
        ocr_controller.validate_detect_language_request(file)

        # Core service handles business logic (asynchronous)
        (
            detected_languages_data,
            primary_language,
            processing_time,
        ) = await LanguageDetectionService.detect_language_in_file(file)

        # Controller handles response formatting (synchronous)
        return ocr_controller.format_detect_language_response(
            detected_languages_data, primary_language, processing_time
        )

    except HTTPException:
        raise
    except Exception as e:
        # Controller handles error formatting (synchronous)
        raise ocr_controller.handle_service_error(e)
