from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel, Field
import time
from datetime import datetime

# Response models
class ExtractTextResponse(BaseModel):
    success: bool = Field(default=True, description="Operation success status")
    extracted_text: str = Field(..., description="The extracted text from the uploaded file")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="OCR confidence score (0-1)")
    processing_time: float = Field(..., description="Time taken to process the file in seconds")

class DetectedLanguage(BaseModel):
    language: str = Field(..., description="Language name")
    language_code: str = Field(..., description="ISO 639-1 language code")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for this language detection")
    text_percentage: float = Field(..., ge=0.0, le=100.0, description="Percentage of text in this language")

class DetectLanguageResponse(BaseModel):
    success: bool = Field(default=True, description="Operation success status")
    detected_languages: List[DetectedLanguage] = Field(..., description="List of detected languages with confidence scores")
    primary_language: str = Field(..., description="The most dominant language detected")
    processing_time: float = Field(..., description="Time taken to process the file in seconds")

class ErrorResponse(BaseModel):
    success: bool = Field(default=False, description="Operation success status")
    error: str = Field(..., description="Error message describing what went wrong")
    error_code: str = Field(..., description="Machine-readable error code")
    timestamp: datetime = Field(default_factory=datetime.now, description="ISO 8601 timestamp when the error occurred")

# Initialize FastAPI app
app = FastAPI(
    title="OCR Toolkit API",
    description="API for optical character recognition operations including text extraction and language detection",
    version="1.0.0",
    contact={
        "name": "OCR Toolkit",
        "email": "support@ocr-toolkit.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {"message": "OCR Toolkit API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post(
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

@app.post(
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
