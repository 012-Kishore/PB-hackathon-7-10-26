# Face Mask Detection Backend (MobileNetV2)

Production-ready Python / FastAPI backend for the **"Face Mask Detection using Transfer Learning with MobileNetV2"** hackathon project.

---

## 👥 Hackathon Team Division of Responsibilities

| Team Member | Domain | Responsibility |
|---|---|---|
| **Member 1** | Machine Learning | Dataset collection, MobileNetV2 transfer learning, model training, evaluation, saving `mask_detector.keras` |
| **Member 2** | Frontend | React website UI, browser webcam stream (`getUserMedia`), frame capture, consuming API and displaying results |
| **Member 3 (This Repository)** | Backend & CV | FastAPI service, OpenCV image decoding & MobileNetV2 preprocessing pipeline, model loading, REST API endpoints, CORS, test suite |

---

## 🏗️ Architecture & Data Flow

```text
Browser Webcam (MediaDevices / getUserMedia)
                       ↓
         React Frontend (Member 2)
  [Captures frame from <canvas> / <video>]
                       ↓
     HTTP POST /predict (multipart/form-data)
                       ↓
               FastAPI Backend
                       ↓
          OpenCV (cv2) Decoding
  [Raw bytes -> BGR numpy array validation]
                       ↓
       OpenCV Face Detection (Haar Cascade)
  [Localizes face ROI bounding box or full image fallback]
                       ↓
        MobileNetV2 Preprocessing
  [BGR to RGB -> Resize (224, 224) -> Scale to [-1, 1] -> Batch (1, 224, 224, 3)]
                       ↓
         MobileNetV2 Model Inference
        (Member 1's trained Keras model)
                       ↓
         Formatted JSON Response
     {"prediction": "Mask", "confidence": 0.964, "class_index": 0}
                       ↓
             React UI Display
```

---

## 📁 Project Structure

```text
backend/
├── app.py                     # FastAPI application & route handlers
├── demo_cli.py                # Instant CLI demonstration script (runs inference on sample images)
├── demo_page.py               # Interactive browser demo UI (Webcam stream & drag-and-drop)
├── services/
│   ├── __init__.py
│   ├── detector.py            # Model loading, inference, and response formatting
│   └── preprocessing.py       # OpenCV decoding & MobileNetV2 tensor preprocessing
├── model/
│   ├── README.md              # Model specification and architecture documentation
│   ├── mask_detector.keras    # Production-ready MobileNetV2 transfer learning model
│   └── train_or_export.py     # Transfer learning architecture build & export pipeline
├── samples/                   # Evaluation & demonstration test images
│   ├── with_mask_sample.png   # Verification image with face mask
│   └── without_mask_sample.jpg# Verification image without face mask
├── requirements.txt           # Python dependencies
├── .env.example               # Configurable environment variables template
├── test_api.py                # Automated test suite (6 test suites)
└── README.md                  # Complete API & integration documentation
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.10 - 3.13)
- pip

### 2. Install Dependencies
Navigate into the `backend` directory and install the required dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Default configuration values:
```env
HOST=0.0.0.0
PORT=8000
MODEL_PATH=model/mask_detector.keras
IMG_SIZE=224
CLASS_NAMES=Mask,Without Mask
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173
```

---

## 🧠 Model Placement (Instructions for Member 1)

When Member 1 finishes training the MobileNetV2 transfer learning model:

1. Save the model in Keras format:
   ```python
   model.save("backend/model/mask_detector.keras")
   ```
2. Ensure the model expects an input shape of `(224, 224, 3)` with MobileNetV2 normalization (`[-1, 1]`).
3. If Member 1's class order differs from `Index 0: Mask, Index 1: Without Mask`, set `CLASS_NAMES` in `.env` accordingly (e.g. `CLASS_NAMES=Without Mask,Mask`).

> **Note on Missing Model:** If the model file is not yet placed in `backend/model/`, the backend starts up gracefully without crashing, logs a clear warning, and indicates `model_loaded: false` on `GET /health`.

---

## 🚀 Running and Demonstrating the Project

### Option A: Instant CLI Demonstration (Fastest)
Run inference directly on sample images in your terminal without needing a web server:

```bash
cd backend
python demo_cli.py
```
Or test a custom image:
```bash
python demo_cli.py --image samples/with_mask_sample.png
```

---

### Option B: Interactive Browser Web Demo (Recommended)
Start the FastAPI server:

```bash
cd backend
python app.py
```

Then open your browser at:
- **Interactive Web Demo**: [`http://localhost:8000/demo`](http://localhost:8000/demo)
  - Features real-time webcam detection (2 FPS, live HUD badge, green/red status)
  - Drag-and-drop image file upload
  - One-click sample test buttons ("Sample 1: With Mask", "Sample 2: Without Mask")
- **Swagger Interactive API UI**: [`http://localhost:8000/docs`](http://localhost:8000/docs)
- **API Health Check**: [`http://localhost:8000/health`](http://localhost:8000/health)
- **OpenAPI JSON Spec**: [`http://localhost:8000/openapi.json`](http://localhost:8000/openapi.json)

---

## 📡 API Contract (For Member 2 / React Frontend)

### 1. Health Check & Model Status

Checks if the backend is running and whether Member 1's model has been loaded.

- **URL**: `/health`
- **Method**: `GET`
- **Response `200 OK`**:
  ```json
  {
    "status": "ok",
    "model_loaded": true
  }
  ```

---

### 2. Predict Face Mask

Sends an image captured from the React webcam stream for mask classification.

- **URL**: `/predict`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Field Name**: `file` (binary image data / Blob)

#### ✅ Success Response (`200 OK`)
```json
{
  "prediction": "Mask",
  "confidence": 0.985,
  "class_index": 0,
  "face_detected": true,
  "box": [454, 183, 57, 57]
}
```

Field descriptions:
- `prediction` (*string*): `"Mask"` or `"Without Mask"`
- `confidence` (*float*): Detection confidence score (between `0.0` and `1.0`, rounded to 4 decimals)
- `class_index` (*int*): Predicted class index (`0` for Mask, `1` for Without Mask)
- `face_detected` (*bool*): `true` if a face ROI was localized, `false` if full image fallback was used
- `box` (*array of ints or null*): Bounding box `[x, y, w, h]` of detected face

#### ❌ Error Responses

- **`400 Bad Request`** (Invalid or unreadable image upload):
  ```json
  {
    "detail": "Failed to decode image. Ensure the file is a valid image (JPEG, PNG, WebP)."
  }
  ```

- **`503 Service Unavailable`** (Model not placed in `backend/model/` yet):
  ```json
  {
    "detail": "Model is not loaded. Please ensure Member 1's trained model is placed at 'backend/model/mask_detector.keras'."
  }
  ```

- **`500 Internal Server Error`** (Inference error):
  ```json
  {
    "detail": "An error occurred while processing the prediction."
  }
  ```

---

## 💻 React Integration Guide (For Member 2)

Member 2 will capture frames from the browser's webcam video element using a canvas and send them to `POST /predict`.

### Implementation Example (Standard Fetch API)

```javascript
// Function to capture a frame from an HTML5 <video> element and send to backend
async function sendWebcamFrameForPrediction(videoElement) {
  // 1. Draw video frame onto a temporary canvas
  const canvas = document.createElement("canvas");
  canvas.width = videoElement.videoWidth || 640;
  canvas.height = videoElement.videoHeight || 480;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

  // 2. Convert canvas frame to JPEG Blob
  canvas.toBlob(async (blob) => {
    if (!blob) return;

    // 3. Prepare multipart/form-data payload
    const formData = new FormData();
    formData.append("file", blob, "webcam_frame.jpg");

    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Prediction Error:", errorData.detail);
        return;
      }

      const data = await response.json();
      console.log("Prediction Result:", data);
      // Example output: { prediction: "Mask", confidence: 0.964, class_index: 0 }

      // 4. Update React State
      // setPrediction(data.prediction);
      // setConfidence(data.confidence);
    } catch (err) {
      console.error("Network error connecting to backend:", err);
    }
  }, "image/jpeg", 0.85);
}
```

### Polling / Interval Recommendation for Live Detection
To achieve smooth real-time detection without overloading the network or the browser:
```javascript
// Trigger a frame capture every 500ms (2 FPS is optimal for real-time mask detection)
useEffect(() => {
  const intervalId = setInterval(() => {
    if (videoRef.current && videoRef.current.readyState === 4) {
      sendWebcamFrameForPrediction(videoRef.current);
    }
  }, 500);

  return () => clearInterval(intervalId);
}, []);
```

---

## 🧪 Running the Backend Tests

The backend includes an automated test suite verifying:
- Image decoding with OpenCV
- MobileNetV2 tensor preprocessing (shape, normalization)
- `GET /health` endpoint
- Graceful `503` handling when model is missing
- Full end-to-end inference pipeline

Run the test suite:
```bash
python test_api.py
```
