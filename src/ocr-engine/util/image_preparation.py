from typing import Optional, Tuple

import cv2


def image_preparation(
    image_buffer: bytes,
    resize: bool = False,
    enhance_contrast: bool = False,
    binarization: bool = False,
    edge_enhancement: bool = False,
    color_inversion: bool = False,
    noise_removal: bool = False,
    cropping: Optional[Tuple[int, int, int, int]] = None,
    image_format: str = "jpeg",
) -> Optional[bytes]:
    """
    Apply a series of preprocessing transformations to an image for OCR improvement.
    Args:
        image_buffer: Input image as bytes (raw buffer).
        resize: If True, upscale image by 2x (only if final size is within limit).
        enhance_contrast: If True, apply CLAHE for contrast enhancement.
        binarization: If True, apply adaptive thresholding.
        edge_enhancement: If True, apply edge enhancement filter.
        color_inversion: If True, invert image colors.
        noise_removal: If True, apply median blur for noise removal.
        cropping: If not None, should be (x, y, w, h) to crop the image.
        image_format: Output format ("jpeg", "png", etc.).
    Returns:
        Transformed image as bytes, or None if size limit exceeded.
    """
    import numpy as np

    from util.config import get_config_value

    # Get processing size limit from config/env
    try:
        size_limit = int(get_config_value("IMAGE_SIZE_PROCESSING_LIMIT", "41943040"))
    except Exception:
        size_limit = 41943040  # fallback 40MB

    # Decode image from buffer
    arr = np.frombuffer(image_buffer, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    if img is None:
        return None

    result = img.copy()

    # Estimate size after resize (if requested)
    if resize:
        h, w = result.shape[:2]
        channels = 1 if len(result.shape) == 2 else result.shape[2]
        est_size = (h * 2) * (w * 2) * channels
        if est_size > size_limit:
            resize = False  # skip resize if would exceed limit
        else:
            result = cv2.resize(result, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    if enhance_contrast:
        if len(result.shape) == 2:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            result = clahe.apply(result)
        else:
            lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l2 = clahe.apply(l)
            lab = cv2.merge((l2, a, b))
            result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    if binarization:
        gray = (
            result
            if len(result.shape) == 2
            else cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        )
        result = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10
        )

    if edge_enhancement:
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        result = cv2.filter2D(result, -1, kernel)

    if color_inversion:
        result = cv2.bitwise_not(result)

    if noise_removal:
        result = cv2.medianBlur(result, 3)

    if cropping:
        x, y, w, h = cropping
        result = result[y : y + h, x : x + w]

    # Encode back to buffer
    ret, buf = cv2.imencode(f".{image_format}", result)
    if not ret:
        return None
    # Check final buffer size
    if len(buf) > size_limit:
        return None
    return buf.tobytes()
