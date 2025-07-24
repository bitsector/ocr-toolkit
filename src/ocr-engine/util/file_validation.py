"""
File content validation utilities for security and integrity checks.

This module provides functions to validate file contents before processing
to prevent malicious files from being processed by OCR engines.
"""

import io

import fitz  # PyMuPDF
from fastapi import HTTPException
from PIL import Image

from util.logger import get_service_logger

logger = get_service_logger(__name__)


def validate_file_contents(
    file_content: bytes, filename: str, content_type: str
) -> bool:
    """
    Validate file contents to ensure they are safe for processing.

    This function performs security checks on file contents including:
    - File signature/magic number validation
    - File structure integrity checks
    - Size and dimension limits
    - Protection against malicious files

    Args:
        file_content: The raw file content as bytes
        filename: Original filename for error reporting
        content_type: MIME type of the file

    Returns:
        bool: True if file is safe to process

    Raises:
        HTTPException: If file is invalid or potentially malicious
    """
    logger.debug(f"Validating file contents for {filename} (type: {content_type})")

    if not file_content:
        raise HTTPException(status_code=400, detail="Empty file content")

    if len(file_content) < 10:
        raise HTTPException(status_code=400, detail="File too small to be valid")

    try:
        if content_type == "application/pdf":
            _validate_pdf_content(file_content, filename)
        elif content_type in ["image/jpeg", "image/jpg"]:
            _validate_jpeg_content(file_content, filename)
        elif content_type == "image/png":
            _validate_png_content(file_content, filename)
        elif content_type == "image/webp":
            _validate_webp_content(file_content, filename)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported content type for validation: {content_type}",
            )

        # Additional PIL-based validation for images
        if content_type.startswith("image/"):
            _validate_image_with_pil(file_content, filename)

        logger.debug(f"File content validation passed for {filename}")
        return True

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File validation failed for {filename}: {str(e)}")
        raise HTTPException(status_code=422, detail=f"File validation failed: {str(e)}")


def _validate_pdf_content(file_content: bytes, filename: str) -> None:
    """Validate PDF file content and structure."""
    # Check PDF magic number
    if not file_content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400, detail="Invalid PDF file: missing PDF header"
        )

    # Try to open with PyMuPDF to validate structure
    try:
        doc = fitz.open(stream=file_content, filetype="pdf")

        # Basic sanity checks
        if doc.page_count == 0:
            doc.close()
            raise HTTPException(status_code=400, detail="Invalid PDF: no pages found")

        if doc.page_count > 100:  # Reasonable limit
            doc.close()
            raise HTTPException(
                status_code=400, detail="PDF has too many pages (limit: 100)"
            )

        # Check first page to ensure it's readable
        try:
            page = doc[0]
            rect = page.rect

            # Reasonable dimension limits (in points, 72 DPI)
            max_dimension = 14400  # 200 inches at 72 DPI
            if rect.width > max_dimension or rect.height > max_dimension:
                doc.close()
                raise HTTPException(
                    status_code=400, detail="PDF page dimensions too large"
                )

        except Exception as e:
            doc.close()
            raise HTTPException(
                status_code=400, detail=f"Invalid PDF structure: {str(e)}"
            )

        doc.close()

    except fitz.fitz.FileDataError as e:
        raise HTTPException(status_code=400, detail=f"Corrupted PDF file: {str(e)}")


def _validate_jpeg_content(file_content: bytes, filename: str) -> None:
    """Validate JPEG file content and structure."""
    # Check JPEG magic number
    if not (
        file_content.startswith(b"\xff\xd8\xff") and file_content.endswith(b"\xff\xd9")
    ):
        raise HTTPException(
            status_code=400, detail="Invalid JPEG file: incorrect file signature"
        )


def _validate_png_content(file_content: bytes, filename: str) -> None:
    """Validate PNG file content and structure."""
    # Check PNG magic number
    png_signature = b"\x89PNG\r\n\x1a\n"
    if not file_content.startswith(png_signature):
        raise HTTPException(
            status_code=400, detail="Invalid PNG file: incorrect file signature"
        )

    # Basic PNG structure validation
    if len(file_content) < 33:  # Minimum PNG file size
        raise HTTPException(status_code=400, detail="Invalid PNG file: file too small")


def _validate_webp_content(file_content: bytes, filename: str) -> None:
    """Validate WebP file content and structure."""
    # Check WebP magic number
    if not (file_content.startswith(b"RIFF") and b"WEBP" in file_content[:12]):
        raise HTTPException(
            status_code=400, detail="Invalid WebP file: incorrect file signature"
        )


def _validate_image_with_pil(file_content: bytes, filename: str) -> None:
    """Additional validation using PIL/Pillow."""
    try:
        with Image.open(io.BytesIO(file_content)) as img:
            # Verify the image can be loaded
            img.verify()

            # Reopen for dimension checks (verify() makes image unusable)
            img = Image.open(io.BytesIO(file_content))

            # Check dimensions
            max_dimension = 20000  # 20k pixels max
            if img.width > max_dimension or img.height > max_dimension:
                raise HTTPException(
                    status_code=400,
                    detail=f"Image dimensions too large: {img.width}x{img.height} (max: {max_dimension})",
                )

            # Check for reasonable file size vs dimensions ratio
            expected_min_size = (img.width * img.height) // 100  # Very rough estimate
            if len(file_content) < expected_min_size:
                logger.warning(
                    f"Suspiciously small file size for dimensions: {filename}"
                )

            logger.debug(
                f"Image validation passed: {img.width}x{img.height}, format: {img.format}"
            )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")


def get_file_info(file_content: bytes, content_type: str) -> dict:
    """
    Get safe file information without full processing.

    Args:
        file_content: The raw file content
        content_type: MIME type of the file

    Returns:
        dict: File information including dimensions, format, etc.
    """
    info = {
        "size_bytes": len(file_content),
        "content_type": content_type,
    }

    try:
        if content_type.startswith("image/"):
            with Image.open(io.BytesIO(file_content)) as img:
                info.update(
                    {
                        "width": img.width,
                        "height": img.height,
                        "format": img.format,
                        "mode": img.mode,
                    }
                )
        elif content_type == "application/pdf":
            doc = fitz.open(stream=file_content, filetype="pdf")
            info.update(
                {
                    "pages": doc.page_count,
                    "pdf_version": doc.metadata.get("format", "Unknown"),
                }
            )
            doc.close()

    except Exception as e:
        logger.warning(f"Could not extract file info: {str(e)}")
        info["info_error"] = str(e)

    return info
