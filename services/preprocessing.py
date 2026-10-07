"""Image preprocessing service for Face Mask Detection using MobileNetV2.

Handles image decoding via OpenCV, color space conversion, resizing,
and MobileNetV2-specific normalization.
"""

import logging
from typing import Optional, Tuple
import cv2
import numpy as np
import tensorflow as tf

logger = logging.getLogger("preprocessing")

_face_cascade: Optional[cv2.CascadeClassifier] = None


class PreprocessingError(Exception):
    """Base exception for preprocessing errors."""
    pass


class InvalidImageError(PreprocessingError):
    """Raised when an uploaded file cannot be decoded as an image."""
    pass


def get_face_cascade() -> Optional[cv2.CascadeClassifier]:
    """Lazy-load OpenCV Haar Cascade classifier for face detection."""
    global _face_cascade
    if _face_cascade is None:
        try:
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            cascade = cv2.CascadeClassifier(cascade_path)
            if not cascade.empty():
                _face_cascade = cascade
            else:
                logger.warning("Loaded face cascade is empty: %s", cascade_path)
        except Exception as exc:
            logger.warning("Failed to initialize OpenCV face cascade: %s", exc)
            _face_cascade = None
    return _face_cascade


def detect_face_roi(
    image_bgr: np.ndarray,
    padding_ratio: float = 0.1,
) -> Tuple[np.ndarray, Optional[Tuple[int, int, int, int]], bool]:
    """Detect the primary face ROI in an image using OpenCV Haar cascade.

    Args:
        image_bgr: Decoded image in OpenCV BGR format.
        padding_ratio: Margin fraction added around detected face box.

    Returns:
        Tuple:
            - roi_bgr (np.ndarray): Extracted face ROI (or full image if no face detected).
            - box (Tuple[int, int, int, int] or None): Bounding box (x, y, w, h) of face.
            - face_detected (bool): True if a face was localized, False if fallback was used.
    """
    try:
        cascade = get_face_cascade()
        if cascade is None:
            return image_bgr, None, False

        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        if len(faces) == 0:
            return image_bgr, None, False

        # Select the largest face box (w * h)
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = [int(v) for v in largest_face]

        # Add padding around face box while staying within image bounds
        img_h, img_w = image_bgr.shape[:2]
        pad_x = int(w * padding_ratio)
        pad_y = int(h * padding_ratio)

        x1 = max(0, x - pad_x)
        y1 = max(0, y - pad_y)
        x2 = min(img_w, x + w + pad_x)
        y2 = min(img_h, y + h + pad_y)

        roi = image_bgr[y1:y2, x1:x2]
        if roi.size == 0:
            return image_bgr, (x, y, w, h), True

        return roi, (x, y, w, h), True

    except Exception as exc:
        logger.debug("Face detection encountered an issue, falling back to full image: %s", exc)
        return image_bgr, None, False


def decode_image(image_bytes: bytes) -> np.ndarray:
    """Decode raw image bytes into an OpenCV BGR numpy array.

    Args:
        image_bytes: Raw bytes from the uploaded file.

    Returns:
        np.ndarray: Decoded image in BGR format (H, W, 3).

    Raises:
        InvalidImageError: If the bytes are empty or cannot be decoded.
    """
    if not image_bytes or len(image_bytes) == 0:
        raise InvalidImageError("Uploaded file is empty.")

    # Convert bytes to 1D uint8 numpy array
    byte_array = np.frombuffer(image_bytes, dtype=np.uint8)

    # Decode image using OpenCV
    image_bgr = cv2.imdecode(byte_array, cv2.IMREAD_COLOR)

    if image_bgr is None or image_bgr.size == 0:
        raise InvalidImageError(
            "Failed to decode image. Ensure the file is a valid image (JPEG, PNG, WebP)."
        )

    return image_bgr


def preprocess_image(
    image_bgr: np.ndarray,
    target_size: Tuple[int, int] = (224, 224)
) -> np.ndarray:
    """Preprocess an OpenCV BGR image for MobileNetV2 model inference.

    Steps:
    1. Convert color format from BGR to RGB (OpenCV uses BGR, MobileNetV2 expects RGB).
    2. Resize to expected input size (default 224x224).
    3. Apply MobileNetV2 preprocessing (scales pixels to [-1, 1]).
    4. Add batch dimension -> shape (1, target_h, target_w, 3).

    Args:
        image_bgr: Input image in OpenCV BGR format.
        target_size: Tuple of (height, width) expected by the model.

    Returns:
        np.ndarray: 4D numpy array ready for model prediction, shape (1, H, W, 3).

    Raises:
        PreprocessingError: If preprocessing fails.
    """
    try:
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        # Resize to target dimension (width, height for cv2.resize)
        target_w, target_h = target_size[1], target_size[0]
        image_resized = cv2.resize(
            image_rgb,
            (target_w, target_h),
            interpolation=cv2.INTER_LINEAR
        )

        # Cast to float32
        image_float = image_resized.astype(np.float32)

        # Apply official MobileNetV2 preprocessing: scales [0, 255] to [-1, 1]
        image_normalized = tf.keras.applications.mobilenet_v2.preprocess_input(image_float)

        # Add batch dimension: (H, W, 3) -> (1, H, W, 3)
        batch = np.expand_dims(image_normalized, axis=0)

        return batch

    except Exception as exc:
        raise PreprocessingError(f"Error during image preprocessing: {str(exc)}") from exc


def process_image_bytes(
    image_bytes: bytes,
    target_size: Tuple[int, int] = (224, 224),
    detect_faces: bool = True,
) -> Tuple[np.ndarray, Optional[Tuple[int, int, int, int]], bool]:
    """Decode raw image bytes, optionally detect/crop face ROI, and preprocess for MobileNetV2.

    Full pipeline:
    Image bytes -> OpenCV decode -> Face detection (Haar cascade) -> ROI crop/resize -> MobileNetV2 Normalization

    Args:
        image_bytes: Raw bytes from uploaded file.
        target_size: Tuple of (height, width) for model input.
        detect_faces: Whether to detect and crop face region before inference.

    Returns:
        Tuple:
            - batch (np.ndarray): Preprocessed 4D batch tensor of shape (1, H, W, 3).
            - box (Tuple[int, int, int, int] or None): Detected face bounding box [x, y, w, h].
            - face_detected (bool): Whether a face was detected.
    """
    image_bgr = decode_image(image_bytes)

    if detect_faces:
        roi_bgr, box, face_detected = detect_face_roi(image_bgr)
        batch = preprocess_image(roi_bgr, target_size=target_size)
        return batch, box, face_detected

    batch = preprocess_image(image_bgr, target_size=target_size)
    return batch, None, False
