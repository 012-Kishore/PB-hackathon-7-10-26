# Face Mask Detection – Machine Learning

## Overview

This module contains the machine learning model for detecting whether a person is wearing a face mask.

The model uses **MobileNetV2 pretrained on ImageNet** with additional classification layers.

## Dataset

The dataset contains two classes:

* `with_mask`
* `without_mask`

Total images: **7,553**

* Training images: **6,043**
* Validation images: **1,510**

## Model

* Architecture: MobileNetV2
* Pretrained weights: ImageNet
* Input size: 224 × 224 × 3
* Classification: 2 classes
* Optimizer: Adam
* Loss: Sparse Categorical Crossentropy
* Epochs: 5

## Training

The model was trained using Google Colab with TensorFlow/Keras.

Training and validation accuracy/loss graphs are available in the `results` folder.

## Evaluation

The model was evaluated using the validation dataset.

A confusion matrix is available at:

`results/confusion_matrix.png`

## Trained Model

The trained model is saved as:

`model/mask_detector.keras`

This `.keras` file is the actual trained model and can be used by the application for mask detection.

## Files

```text
ml/
├── training.ipynb
├── model/
│   └── mask_detector.keras
├── results/
│   ├── accuracy.png
│   ├── loss.png
│   └── confusion_matrix.png
└── README.md
```
