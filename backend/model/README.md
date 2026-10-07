# Model Directory

This directory contains the production-ready MobileNetV2 transfer learning model.

### Model Details
- **Filename**: `mask_detector.keras`
- **Format**: Native Keras 3 / TensorFlow 2.16+ format
- **Architecture**: MobileNetV2 Base (ImageNet pre-trained feature extractor) + Custom Classification Head:
  - `AveragePooling2D(pool_size=(7, 7))`
  - `Flatten`
  - `Dense(128, activation='relu')`
  - `Dropout(0.5)`
  - `Dense(2, activation='softmax')`
- **Input Dimensions**: `(224, 224, 3)` with MobileNetV2 scaling `[-1.0, 1.0]`
- **Classes**:
  - `Index 0`: **Mask** (with mask)
  - `Index 1`: **Without Mask** (no mask)
- **Status**: Verified and fully functional. Loaded automatically by `MaskDetector`.

