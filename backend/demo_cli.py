"""Command-line demonstration for Face Mask Detection.

Quickly verifies model inference on test images without requiring a web server.
"""

import argparse
from pathlib import Path
import sys

# Ensure backend root is on Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from services.detector import MaskDetector


def run_demo(image_path: Path, model_path: Path):
    print("=" * 60)
    print("   FACE MASK DETECTION - INFERENCE DEMO (MobileNetV2)")
    print("=" * 60)

    if not image_path.exists():
        print(f"[ERROR] Image not found: {image_path}")
        sys.exit(1)

    print(f"[1] Loading model: {model_path} ...")
    detector = MaskDetector(model_path=str(model_path))
    if not detector.load_model():
        print("[ERROR] Failed to load detector model.")
        sys.exit(1)

    print(f"[2] Reading image: {image_path} ...")
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    print("[3] Performing inference...")
    result = detector.predict(image_bytes)

    prediction = result["prediction"]
    confidence = result["confidence"] * 100
    class_idx = result["class_index"]

    print("\n" + "-" * 40)
    print("   DETECTION RESULT")
    print("-" * 40)
    status_icon = " [OK - MASK ON]" if prediction == "Mask" else " [ALERT - NO MASK]"
    face_info = f"Detected {result.get('box')}" if result.get("face_detected") else "Full image fallback"
    print(f"Prediction : {prediction}{status_icon}")
    print(f"Confidence : {confidence:.2f}%")
    print(f"Face ROI   : {face_info}")
    print(f"Class Index: {class_idx}")
    print("-" * 40 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Demonstrate Face Mask Detector")
    parser.add_argument(
        "--image",
        type=str,
        default=None,
        help="Path to image file (default runs both sample images)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=str(backend_dir / "model" / "mask_detector.keras"),
        help="Path to .keras model file",
    )
    args = parser.parse_args()

    model_path = Path(args.model)

    if args.image:
        run_demo(Path(args.image), model_path)
    else:
        # Run both samples
        samples_dir = backend_dir / "samples"
        mask_sample = samples_dir / "with_mask_sample.png"
        no_mask_sample = samples_dir / "without_mask_sample.jpg"

        print("\n>>> Testing Sample 1: With Mask")
        run_demo(mask_sample, model_path)

        print("\n>>> Testing Sample 2: Without Mask")
        run_demo(no_mask_sample, model_path)


if __name__ == "__main__":
    main()
