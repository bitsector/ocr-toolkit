# Core layer - Business logic for OCR and language detection services
# This layer contains the core business logic, domain rules, and service implementations.
# It's independent of HTTP concerns and can be used by controllers or other interfaces.

import io
import os
import time
from typing import List, Tuple

import fitz  # PyMuPDF for PDF processing
import pytesseract
from fastapi import HTTPException, UploadFile
from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException
from PIL import Image
from PIL.Image import Image as PILImage

from util.config import get_cached_config
from util.logger import get_service_logger

# Initialize logger for this service
logger = get_service_logger(__name__)

# Load configuration
config = get_cached_config()

# Language code mappings for better readability
LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "hi": "Hindi",
    "th": "Thai",
    "vi": "Vietnamese",
    "nl": "Dutch",
    "sv": "Swedish",
    "da": "Danish",
    "no": "Norwegian",
    "fi": "Finnish",
    "pl": "Polish",
    "cs": "Czech",
    "hu": "Hungarian",
    "ro": "Romanian",
    "bg": "Bulgarian",
    "hr": "Croatian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "et": "Estonian",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "mt": "Maltese",
    "ga": "Irish",
    "cy": "Welsh",
}


class FileValidationService:
    """Service for file validation operations"""

    @staticmethod
    def get_allowed_content_types() -> List[str]:
        """Get allowed content types from configuration"""
        return config.allowed_content_types

    @staticmethod
    def get_max_file_size() -> int:
        """Get maximum file size from configuration"""
        return config.max_file_size

    @staticmethod
    async def validate_file(file: UploadFile) -> bytes:
        """
        Validate uploaded file format and size.

        Args:
            file: The uploaded file to validate

        Returns:
            bytes: The file content as bytes

        Raises:
            HTTPException: If file is invalid or too large
        """
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        # If content_type is not set or is generic, try to determine from filename
        content_type = file.content_type
        if content_type in [None, "application/octet-stream"] and file.filename:
            ext = os.path.splitext(file.filename)[1].lower()
            content_type_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp",
                ".pdf": "application/pdf",
            }
            content_type = content_type_map.get(ext)

        # Check file type
        allowed_types = FileValidationService.get_allowed_content_types()
        if content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Only JPEG, PNG, WEBP, and PDF files are supported. Got: {content_type}",
            )

        # Read and check file size
        file_content = await file.read()
        max_size = FileValidationService.get_max_file_size()
        if len(file_content) > max_size:
            max_size_mb = max_size / (1024 * 1024)
            raise HTTPException(
                status_code=413, detail=f"File too large. Maximum size is {max_size_mb:.1f}MB"
            )

        return file_content


class OCRService:
    """Service for OCR text extraction operations"""

    @staticmethod
    def extract_text_from_image(image_bytes: bytes, filename: str) -> Tuple[str, float]:
        """
        Extract text from image using Tesseract OCR.
        Simple approach matching Tesseract.js implementation.

        Args:
            image_bytes: Image data as bytes
            filename: Original filename for error reporting

        Returns:
            Tuple[str, float]: Extracted text and confidence score

        Raises:
            HTTPException: If OCR processing fails
        """
        try:
            # Open image with PIL
            image: PILImage = Image.open(io.BytesIO(image_bytes))
            logger.debug(
                f"Processing image {filename} with size {image.size}, mode: {image.mode}"
            )

            # Convert to RGB if necessary (for WEBP and other formats)
            if image.mode != "RGB":
                image = image.convert("RGB")
                logger.debug("Converted image to RGB mode")

            # Simple OCR extraction - matching Tesseract.js approach
            # Use default Tesseract settings, no custom PSM or OEM
            extracted_text = pytesseract.image_to_string(image).strip()
            logger.debug(f"OCR result for {filename}: '{extracted_text}'")

            # Set confidence based on whether text was found
            confidence_score = config.ocr_confidence_score if extracted_text else config.ocr_no_text_confidence

            return extracted_text, confidence_score

        except Exception as e:
            logger.error(f"OCR failed for {filename}: {str(e)}")
            raise HTTPException(
                status_code=422, detail=f"Failed to process image {filename}: {str(e)}"
            )

    @staticmethod
    def extract_text_from_pdf(pdf_bytes: bytes, filename: str) -> Tuple[str, float]:
        """
        Extract text from PDF using PyMuPDF and OCR for images.

        Args:
            pdf_bytes: PDF data as bytes
            filename: Original filename for error reporting

        Returns:
            Tuple[str, float]: Extracted text and confidence score

        Raises:
            HTTPException: If PDF processing fails
        """
        try:
            # Open PDF document
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

            all_text = []
            all_confidences = []

            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]

                # First try to extract text directly (for text-based PDFs)
                page_text = page.get_text().strip()

                if page_text:
                    # If we have extractable text, use it with high confidence
                    all_text.append(page_text)
                    all_confidences.append(
                        config.pdf_text_confidence
                    )  # High confidence for direct text extraction
                else:
                    # If no text, try OCR on the page image
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")

                    # Use OCR service for the page image
                    ocr_text, ocr_confidence = OCRService.extract_text_from_image(
                        img_data, f"{filename}_page_{page_num + 1}"
                    )

                    if ocr_text.strip():
                        all_text.append(ocr_text)
                        all_confidences.append(ocr_confidence)

            pdf_document.close()

            # Combine all text and calculate average confidence
            combined_text = "\n".join(all_text)
            avg_confidence = (
                sum(all_confidences) / len(all_confidences) if all_confidences else 0.0
            )

            return combined_text, avg_confidence

        except Exception as e:
            raise HTTPException(
                status_code=422, detail=f"Failed to process PDF {filename}: {str(e)}"
            )

    @staticmethod
    async def extract_text(file: UploadFile) -> Tuple[str, float, float]:
        """
        Main entry point for text extraction from any supported file type.

        Args:
            file: The uploaded file to process

        Returns:
            Tuple[str, float, float]: Extracted text, confidence score, and processing time
        """
        start_time = time.time()

        # Validate file
        file_content = await FileValidationService.validate_file(file)

        # Determine content type for processing (similar logic as in validation)
        content_type = file.content_type
        if content_type in [None, "application/octet-stream"] and file.filename:
            ext = os.path.splitext(file.filename)[1].lower()
            content_type_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp",
                ".pdf": "application/pdf",
            }
            content_type = content_type_map.get(ext, content_type)

        # Process based on content type
        if content_type == "application/pdf":
            text, confidence = OCRService.extract_text_from_pdf(
                file_content, file.filename
            )
        else:
            # Handle all image types
            text, confidence = OCRService.extract_text_from_image(
                file_content, file.filename
            )

        processing_time = time.time() - start_time

        if not text.strip():
            # If no text was extracted, return a meaningful message
            text = f"No readable text found in {file.filename}. The image may be too blurry, have poor quality, or contain no text."
            confidence = 0.0

        return text, confidence, processing_time


class LanguageDetectionService:
    """Service for language detection operations"""

    @staticmethod
    def detect_languages(text: str) -> List[dict]:
        """
        Detect languages in the given text.

        Args:
            text: Text to analyze for language detection

        Returns:
            List[dict]: List of detected languages with confidence scores
        """
        if not text.strip():
            return []

        try:
            # Use langdetect to identify languages
            detected_langs = detect_langs(text)

            languages = []
            total_confidence = sum(lang.prob for lang in detected_langs)

            for lang in detected_langs:
                language_name = LANGUAGE_NAMES.get(lang.lang, f"Unknown ({lang.lang})")
                text_percentage = (
                    (lang.prob / total_confidence) * 100 if total_confidence > 0 else 0
                )

                languages.append(
                    {
                        "language": language_name,
                        "language_code": lang.lang,
                        "confidence": lang.prob,
                        "text_percentage": text_percentage,
                    }
                )

            # Sort by confidence (highest first)
            languages.sort(key=lambda x: x["confidence"], reverse=True)

            return languages

        except LangDetectException:
            # If language detection fails, assume English as fallback
            return [
                {
                    "language": config.fallback_language,
                    "language_code": config.fallback_language_code,
                    "confidence": config.language_detection_fallback_confidence,
                    "text_percentage": 100.0,
                }
            ]

    @staticmethod
    async def detect_language_in_file(
        file: UploadFile,
    ) -> Tuple[List[dict], str, float]:
        """
        Detect languages in an uploaded file by first extracting text via OCR.

        Args:
            file: The uploaded file to process

        Returns:
            Tuple[List[dict], str, float]: Detected languages, primary language, and processing time
        """
        start_time = time.time()

        # First extract text from the file
        extracted_text, _, _ = await OCRService.extract_text(file)

        # Then detect languages in the extracted text
        detected_languages = LanguageDetectionService.detect_languages(extracted_text)

        # Determine primary language
        primary_language = (
            detected_languages[0]["language"] if detected_languages else "Unknown"
        )

        processing_time = time.time() - start_time

        return detected_languages, primary_language, processing_time
