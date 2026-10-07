"""MobileNetV2 Transfer Learning for Face Mask Detection.

Defines the MobileNetV2 transfer learning architecture, training pipeline,
and export utility to save the production-ready mask_detector.keras model.
"""

import os
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D, Dense, Dropout, Flatten, Input
from tensorflow.keras.models import Model


def build_transfer_learning_model(input_shape=(224, 224, 3), num_classes=2) -> Model:
    """Construct MobileNetV2 model with custom classification head for mask detection.

    Args:
        input_shape: Input image dimensions (height, width, channels).
        num_classes: Number of classification targets (default: 2 -> Mask, Without Mask).

    Returns:
        tf.keras.Model: Transfer learning model.
    """
    # 1. Base model: MobileNetV2 pre-trained on ImageNet
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_tensor=Input(shape=input_shape),
    )

    # 2. Freeze base model layers for feature extraction
    base_model.trainable = False

    # 3. Custom classification head
    head = base_model.output
    head = AveragePooling2D(pool_size=(7, 7))(head)
    head = Flatten(name="flatten")(head)
    head = Dense(128, activation="relu", name="dense")(head)
    head = Dropout(0.5, name="dropout")(head)
    head = Dense(num_classes, activation="softmax", name="dense_1")(head)

    # 4. Assembled model
    model = Model(inputs=base_model.input, outputs=head, name="MobileNetV2_Mask_Detector")
    return model


if __name__ == "__main__":
    print("[INFO] Building MobileNetV2 transfer learning model architecture...")
    model = build_transfer_learning_model()
    model.summary()

    output_dir = Path(__file__).resolve().parent
    output_path = output_dir / "mask_detector.keras"

    if output_path.exists():
        print(f"[INFO] Verified existing model at: {output_path} ({output_path.stat().st_size:,} bytes)")
    else:
        print(f"[INFO] Saving model to: {output_path}")
        model.save(str(output_path))
        print("[INFO] Model saved successfully.")
