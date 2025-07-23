from pydantic import BaseModel, Field
from typing import List
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
