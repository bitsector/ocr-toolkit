from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
import time
from datetime import datetime

# Import models from the models package
from models import ExtractTextResponse, DetectedLanguage, DetectLanguageResponse, ErrorResponse

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
        400: {"model": ErrorResponse, "description": "Bad request - invalid file format or missing file"},
        413: {"model": ErrorResponse, "description": "File too large"},
        422: {"model": ErrorResponse, "description": "Unprocessable entity - file cannot be processed"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Extract text from image or document",
    description="Uploads a file and extracts all readable text from it using OCR technology. Supports JPEG, PNG, WEBP, and PDF formats.",
    tags=["OCR Operations"]
)
async def extract_text(
    file: UploadFile = File(..., description="Image or document file (supports JPEG, PNG, WEBP, PDF)")
) -> ExtractTextResponse:
    """
    Extract text from an uploaded image or document file.
    
    This endpoint processes the uploaded file and returns the extracted text along with
    confidence scores and processing time metrics.
    """
    start_time = time.time()
    
    try:
        # Validate file
        if not file:
            raise HTTPException(
                status_code=400,
                detail="No file provided"
            )
        
        # Check file type
        allowed_types = ["image/jpeg", "image/png", "image/webp", "application/pdf"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Only JPEG, PNG, WEBP, and PDF files are supported. Got: {file.content_type}"
            )
        
        # Check file size (10MB limit)
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=413,
                detail="File too large. Maximum size is 10MB"
            )
        
        # TODO: Implement actual OCR logic here
        # For now, return placeholder data
        processing_time = time.time() - start_time
        
        return ExtractTextResponse(
            success=True,
            extracted_text=f"This is placeholder extracted text from file: {file.filename}. Implement OCR logic here.",
            confidence_score=0.95,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post(
    "/detect-language",
    response_model=DetectLanguageResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request - invalid file format or missing file"},
        413: {"model": ErrorResponse, "description": "File too large"},
        422: {"model": ErrorResponse, "description": "Unprocessable entity - file cannot be processed"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Detect languages in image or document",
    description="Uploads a file and detects the languages used in the text content. Returns detected languages with confidence scores.",
    tags=["OCR Operations"]
)
async def detect_language(
    file: UploadFile = File(..., description="Image or document file (supports JPEG, PNG, WEBP, PDF)")
) -> DetectLanguageResponse:
    """
    Detect languages in an uploaded image or document file.
    
    This endpoint processes the uploaded file, extracts text, and identifies the languages
    present in the content along with confidence scores and percentages.
    """
    start_time = time.time()
    
    try:
        # Validate file
        if not file:
            raise HTTPException(
                status_code=400,
                detail="No file provided"
            )
        
        # Check file type
        allowed_types = ["image/jpeg", "image/png", "image/webp", "application/pdf"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Only JPEG, PNG, WEBP, and PDF files are supported. Got: {file.content_type}"
            )
        
        # Check file size (10MB limit)
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=413,
                detail="File too large. Maximum size is 10MB"
            )
        
        # TODO: Implement actual language detection logic here
        # For now, return placeholder data
        processing_time = time.time() - start_time
        
        detected_languages = [
            DetectedLanguage(
                language="English",
                language_code="en",
                confidence=0.98,
                text_percentage=85.5
            ),
            DetectedLanguage(
                language="Spanish", 
                language_code="es",
                confidence=0.76,
                text_percentage=14.5
            )
        ]
        
        return DetectLanguageResponse(
            success=True,
            detected_languages=detected_languages,
            primary_language="English",
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
