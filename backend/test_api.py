"""Automated test suite for Face Mask Detection Backend.

Tests:
1. OpenCV Image Decoding & Preprocessing (resizing, MobileNetV2 normalization)
2. Health check endpoint (GET /health)
3. API behavior when model is missing (503 Service Unavailable)
4. Invalid image handling (400 Bad Request)
5. End-to-end model inference pipeline with an ephemeral test model
"""

import os
import sys
import tempfile
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

import cv2
import numpy as np
from fastapi.testclient import TestClient

from app import app, detector
from services.detector import MaskDetector, ModelNotLoadedError
from services.preprocessing import (
    InvalidImageError,
    decode_image,
    detect_face_roi,
    preprocess_image,
    process_image_bytes,
)


def create_sample_image_bytes(width: int = 300, height: int = 300, color: tuple = (0, 128, 255)) -> bytes:
    """Generate a valid JPEG encoded image in memory."""
    img = np.full((height, width, 3), color, dtype=np.uint8)
    success, encoded = cv2.imencode(".jpg", img)
    assert success, "Failed to encode test image"
    return encoded.tobytes()


def test_image_preprocessing():
    """Verify OpenCV decoding, color conversion, resizing, and normalization."""
    raw_bytes = create_sample_image_bytes(width=400, height=300)

    # 1. Test image decoding
    decoded = decode_image(raw_bytes)
    assert decoded.shape == (300, 400, 3)
    assert decoded.dtype == np.uint8

    # 2. Test preprocessing for MobileNetV2
    batch = preprocess_image(decoded, target_size=(224, 224))
    assert batch.shape == (1, 224, 224, 3)
    assert batch.dtype == np.float32

    # MobileNetV2 preprocess_input normalizes [0, 255] to [-1.0, 1.0]
    assert np.all(batch >= -1.0) and np.all(batch <= 1.0)

    # 3. Test invalid image handling
    try:
        decode_image(b"not an image data")
        assert False, "Should have raised InvalidImageError"
    except InvalidImageError:
        pass


def test_health_check_endpoint():
    """Verify GET /health returns status: ok and model_loaded flag."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data


def test_predict_without_model():
    """Verify POST /predict returns 503 when model is not yet placed."""
    client = TestClient(app)
    # Ensure detector model is None for this test
    original_loaded = detector.is_loaded
    detector.is_loaded = False

    sample_bytes = create_sample_image_bytes()
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", sample_bytes, "image/jpeg")},
    )
    assert response.status_code == 503
    assert "Model is not loaded" in response.json()["detail"]

    detector.is_loaded = original_loaded


def test_end_to_end_inference_pipeline():
    """Verify the full MobileNetV2 inference pipeline with an ephemeral test model.

    This ensures that tf.keras.models.load_model, preprocessing, and prediction
    output formatting work end-to-end without bugs.
    """
    import tensorflow as tf

    with tempfile.TemporaryDirectory() as tmp_dir:
        test_model_path = Path(tmp_dir) / "test_mobilenet.keras"

        # Create a MobileNetV2-compatible transfer learning test architecture
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights=None,
        )
        x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
        outputs = tf.keras.layers.Dense(2, activation="softmax")(x)
        test_model = tf.keras.Model(inputs=base_model.input, outputs=outputs)
        test_model.save(str(test_model_path))

        # Instantiate a detector pointing to this model
        test_detector = MaskDetector(
            model_path=str(test_model_path),
            class_names=["Mask", "Without Mask"],
        )
        assert test_detector.load_model() is True
        assert test_detector.is_loaded is True

        # Test prediction with sample image
        sample_bytes = create_sample_image_bytes(250, 250)
        result = test_detector.predict(sample_bytes)

        assert "prediction" in result
        assert result["prediction"] in ["Mask", "Without Mask"]
        assert "confidence" in result
        assert isinstance(result["confidence"], float)
        assert 0.0 <= result["confidence"] <= 1.0
        assert "class_index" in result
        assert result["class_index"] in [0, 1]
        print(f"Test prediction verified successfully: {result}")


def test_demo_and_samples_endpoints():
    """Verify GET /demo returns HTML and GET /samples returns sample images."""
    client = TestClient(app)

    # 1. Test /demo HTML page
    res_demo = client.get("/demo")
    assert res_demo.status_code == 200
    assert "text/html" in res_demo.headers.get("content-type", "")
    assert "Face Mask Detection Demo" in res_demo.text

    # 2. Test /samples endpoints
    res_mask = client.get("/samples/with_mask_sample.png")
    assert res_mask.status_code == 200
    assert len(res_mask.content) > 0

    res_nomask = client.get("/samples/without_mask_sample.jpg")
    assert res_nomask.status_code == 200
    assert len(res_nomask.content) > 0

    # 3. Test non-existent sample
    res_404 = client.get("/samples/does_not_exist.png")
    assert res_404.status_code == 404


def test_real_model_inference_with_samples():
    """Verify live inference against mask_detector.keras with sample images."""
    samples_dir = backend_dir / "samples"
    mask_sample = samples_dir / "with_mask_sample.png"
    no_mask_sample = samples_dir / "without_mask_sample.jpg"

    if not mask_sample.exists() or not no_mask_sample.exists():
        print("[SKIP] Sample images not found for real model test")
        return

    with TestClient(app) as client:
        # Verify model loaded
        res_health = client.get("/health")
        assert res_health.status_code == 200
        assert res_health.json()["model_loaded"] is True

        # Test mask sample
        with open(mask_sample, "rb") as f:
            res_mask = client.post("/predict", files={"file": ("mask.png", f, "image/png")})
        assert res_mask.status_code == 200
        data_mask = res_mask.json()
        assert data_mask["prediction"] == "Mask"
        assert data_mask["class_index"] == 0
        assert data_mask["confidence"] >= 0.70

        # Test without mask sample
        with open(no_mask_sample, "rb") as f:
            res_nomask = client.post("/predict", files={"file": ("no_mask.jpg", f, "image/jpeg")})
        assert res_nomask.status_code == 200
        data_nomask = res_nomask.json()
        assert data_nomask["prediction"] == "Without Mask"
        assert data_nomask["class_index"] == 1
        assert data_nomask["confidence"] >= 0.70

        # Verify face_detected and box fields are present in response
        assert "face_detected" in data_mask
        assert "box" in data_mask
        assert "face_detected" in data_nomask
        assert "box" in data_nomask

        # Test invalid image upload
        res_bad = client.post("/predict", files={"file": ("corrupt.jpg", b"bad image content", "image/jpeg")})
        assert res_bad.status_code == 400


def test_face_detection_pipeline():
    """Verify OpenCV face detection localization and fallback behaviors."""
    # 1. Non-face image should gracefully fall back to full image
    blank = np.full((200, 200, 3), 128, dtype=np.uint8)
    roi, box, detected = detect_face_roi(blank)
    assert detected is False
    assert box is None
    assert roi.shape == (200, 200, 3)

    # 2. Image with face should detect ROI and bounding box
    sample_path = backend_dir / "samples" / "without_mask_sample.jpg"
    if sample_path.exists():
        img = cv2.imread(str(sample_path))
        roi, box, detected = detect_face_roi(img)
        assert detected is True
        assert box is not None
        assert len(box) == 4
        assert roi.size > 0


if __name__ == "__main__":
    print("Running automated backend tests...")
    test_image_preprocessing()
    print("[PASS] Image Preprocessing passed!")

    test_face_detection_pipeline()
    print("[PASS] Face Detection & ROI Fallback passed!")

    test_health_check_endpoint()
    print("[PASS] Health Check Endpoint passed!")

    test_predict_without_model()
    print("[PASS] Missing Model 503 handling passed!")

    test_end_to_end_inference_pipeline()
    print("[PASS] End-to-End Ephemeral Inference Pipeline passed!")

    test_demo_and_samples_endpoints()
    print("[PASS] Web Demo & Sample Image Endpoints passed!")

    test_real_model_inference_with_samples()
    print("[PASS] Real Model Inference on Samples passed!")

    print("\nALL BACKEND TESTS PASSED SUCCESSFULLY!")

