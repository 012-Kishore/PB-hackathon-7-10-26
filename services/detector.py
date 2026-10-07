"""Face mask detector service.

Loads Member 1's trained MobileNetV2 Keras model, handles inference,
and maps predictions to human-readable class labels with confidence scores.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import tensorflow as tf

from services.preprocessing import (
    InvalidImageError,
    PreprocessingError,
    process_image_bytes,
)

logger = logging.getLogger("mask_detector")


class ModelNotLoadedError(Exception):
    """Raised when prediction is requested but model is not loaded."""
    pass


class PredictionError(Exception):
    """Raised when an error occurs during model inference."""
    pass


def resolve_model_path(configured_path: str) -> Path:
    """Resolve the model path across different execution working directories.

    Args:
        configured_path: Relative or absolute path from config/env.

    Returns:
        Path: Resolved filesystem path.
    """
    path = Path(configured_path)
    if path.is_absolute() and path.exists():
        return path

    # Check relative to current working directory
    cwd_path = Path.cwd() / path
    if cwd_path.exists():
        return cwd_path

    # Check relative to the backend package root (parent of services directory)
    backend_root = Path(__file__).resolve().parent.parent
    backend_rel_path = backend_root / path
    if backend_rel_path.exists():
        return backend_rel_path

    # Also check if configured_path starts with 'backend/' and we are already in backend/
    if str(path).startswith("backend") or str(path).startswith("backend/"):
        stripped = Path(*path.parts[1:])
        if (backend_root / stripped).exists():
            return backend_root / stripped
        if (Path.cwd() / stripped).exists():
            return Path.cwd() / stripped

    # Default fallback: return path relative to backend root
    return backend_root / path


class MaskDetector:
    """Manages MobileNetV2 model loading and prediction for face mask detection."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        class_names: Optional[List[str]] = None,
        target_size: Tuple[int, int] = (224, 224),
    ):
        """Initialize the mask detector.

        Args:
            model_path: Path to the .keras / .h5 model file.
            class_names: List of class labels in index order.
            target_size: Target image (H, W) for the model.
        """
        # Default to environment variable or standard model directory
        self.model_path_str = model_path or os.getenv(
            "MODEL_PATH", "model/mask_detector.keras"
        )
        self.target_size = target_size

        # Class labels (default: Index 0 -> 'Mask', Index 1 -> 'Without Mask')
        if class_names:
            self.class_names = class_names
        else:
            env_classes = os.getenv("CLASS_NAMES")
            if env_classes:
                self.class_names = [c.strip() for c in env_classes.split(",") if c.strip()]
            else:
                self.class_names = ["Mask", "Without Mask"]

        self.model: Optional[tf.keras.Model] = None
        self.resolved_path: Optional[Path] = None
        self.is_loaded: bool = False

    def load_model(self) -> bool:
        """Load the trained Keras model from disk.

        Returns:
            bool: True if loaded successfully, False if model file is missing or invalid.
        """
        self.resolved_path = resolve_model_path(self.model_path_str)

        if not self.resolved_path.exists():
            logger.warning(
                "==========================================================\n"
                "[STARTUP NOTICE] Trained model file NOT FOUND at:\n"
                "  -> %s\n"
                "Please place Member 1's trained 'mask_detector.keras' file into\n"
                "the 'backend/model/' directory or set MODEL_PATH in your .env file.\n"
                "The server will continue running. /health will report model_loaded=false\n"
                "and /predict will return HTTP 503 until the model is provided.\n"
                "==========================================================",
                self.resolved_path.resolve(),
            )
            self.model = None
            self.is_loaded = False
            return False

        try:
            logger.info("Loading trained model from %s ...", self.resolved_path)
            self.model = tf.keras.models.load_model(str(self.resolved_path))
            self.is_loaded = True
            logger.info(
                "Model loaded successfully! Expected input: %s, Classes: %s",
                self.target_size,
                self.class_names,
            )
            return True
        except Exception as exc:
            logger.error(
                "Failed to load model from %s. Error: %s",
                self.resolved_path,
                str(exc),
                exc_info=True,
            )
            self.model = None
            self.is_loaded = False
            return False

    def predict(self, image_bytes: bytes, detect_faces: bool = True) -> Dict[str, Any]:
        """Perform mask detection prediction on uploaded raw image bytes.

        Pipeline:
        image_bytes -> face detection -> ROI preprocessing -> MobileNetV2 -> prediction

        Args:
            image_bytes: Raw image bytes from HTTP request.
            detect_faces: Whether to detect and crop face ROI prior to classification.

        Returns:
            Dict containing 'prediction', 'confidence', 'class_index', 'face_detected', and 'box'.

        Raises:
            ModelNotLoadedError: If the model has not been loaded.
            InvalidImageError: If the image cannot be decoded.
            PreprocessingError: If preprocessing fails.
            PredictionError: If inference fails.
        """
        if not self.is_loaded or self.model is None:
            raise ModelNotLoadedError(
                "Model is not loaded. Please ensure Member 1's trained model is "
                f"placed at '{self.resolved_path or self.model_path_str}'."
            )

        # 1. Decode & Preprocess image into batch tensor (1, 224, 224, 3) with face ROI detection
        input_batch, box, face_detected = process_image_bytes(
            image_bytes,
            target_size=self.target_size,
            detect_faces=detect_faces,
        )

        # 2. Model inference
        try:
            raw_predictions = self.model.predict(input_batch, verbose=0)
        except Exception as exc:
            raise PredictionError(f"Model prediction failed: {str(exc)}") from exc

        # 3. Interpret prediction output
        result = self._format_prediction(raw_predictions)
        result["face_detected"] = bool(face_detected)
        result["box"] = list(box) if box is not None else None
        return result

    def _format_prediction(self, raw_predictions: np.ndarray) -> Dict[str, Any]:
        """Convert raw model output to standard response contract.

        Handles both:
        - 2-unit softmax / probabilities: shape (1, 2)
        - 1-unit binary sigmoid: shape (1, 1) or (1,)

        Args:
            raw_predictions: Output tensor from model.predict().

        Returns:
            Dict with prediction, confidence, class_index.
        """
        preds = np.array(raw_predictions)

        # Case A: Multi-class / 2-class softmax (shape (1, N) with N >= 2)
        if preds.ndim == 2 and preds.shape[1] >= 2:
            probabilities = preds[0]
            # If raw logits, apply softmax
            if not np.isclose(np.sum(probabilities), 1.0, atol=1e-2):
                exp_probs = np.exp(probabilities - np.max(probabilities))
                probabilities = exp_probs / np.sum(exp_probs)

            class_idx = int(np.argmax(probabilities))
            confidence = float(probabilities[class_idx])

        # Case B: Binary classification with single sigmoid output (shape (1, 1) or (1,))
        elif (preds.ndim == 2 and preds.shape[1] == 1) or (preds.ndim == 1 and preds.shape[0] == 1):
            prob = float(preds.reshape(-1)[0])
            if prob < 0.5:
                class_idx = 0
                confidence = 1.0 - prob
            else:
                class_idx = 1
                confidence = prob
        else:
            raise PredictionError(f"Unexpected model output shape: {preds.shape}")

        # Map to class name
        if 0 <= class_idx < len(self.class_names):
            label = self.class_names[class_idx]
        else:
            label = f"Class_{class_idx}"

        return {
            "prediction": label,
            "confidence": round(float(confidence), 4),
            "class_index": class_idx,
        }
