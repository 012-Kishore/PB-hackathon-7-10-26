"""FastAPI application for Face Mask Detection using MobileNetV2.

Provides REST APIs for:
- Health checking and model status (GET /health)
- Image-based face mask prediction (POST /predict)
- Interactive OpenAPI documentation (/docs, /redoc)
"""

from contextlib import asynccontextmanager
import logging
import os
import sys
from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

# Ensure local services can be imported regardless of execution directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from services.detector import (
    MaskDetector,
    ModelNotLoadedError,
    PredictionError,
)
from services.preprocessing import (
    InvalidImageError,
    PreprocessingError,
)
from demo_page import DEMO_HTML

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("face_mask_api")

# Global detector instance
detector = MaskDetector()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager.

    Loads Member 1's trained MobileNetV2 model at server startup.
    """
    logger.info("Initializing Face Mask Detection Service...")
    success = detector.load_model()
    if success:
        logger.info("Face Mask Detector is READY for predictions.")
    else:
        logger.warning(
            "Service started WITHOUT trained model. "
            "/health will indicate model_loaded=False. "
            "/predict will return 503 until Member 1's model is placed in 'model/'."
        )
    yield
    logger.info("Shutting down Face Mask Detection Service...")


# Initialize FastAPI app with descriptive metadata
app = FastAPI(
    title="Face Mask Detection API",
    description=(
        "Backend REST API for Face Mask Detection using Transfer Learning with MobileNetV2.\n\n"
        "- Built for React frontend webcam integration (Member 2).\n"
        "- Connects with Member 1's trained MobileNetV2 Keras model.\n"
        "- Preprocesses images with OpenCV and MobileNetV2 normalization."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS Configuration (for Member 2's React frontend)
# ---------------------------------------------------------------------------
def get_cors_origins() -> List[str]:
    """Parse CORS origins from environment variable or apply safe defaults."""
    cors_env = os.getenv("CORS_ORIGINS")
    if cors_env:
        origins = [o.strip() for o in cors_env.split(",") if o.strip()]
        return origins
    return [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Response Schemas
# ---------------------------------------------------------------------------
class HealthResponse(BaseModel):
    """Response model for GET /health."""
    status: str = Field(..., description="API operational status", examples=["ok"])
    model_loaded: bool = Field(..., description="Whether Member 1's model is loaded", examples=[True])


class PredictionResponse(BaseModel):
    """Response model for POST /predict."""
    prediction: str = Field(..., description="Predicted class label ('Mask' or 'Without Mask')", examples=["Mask"])
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0", examples=[0.964])
    class_index: int = Field(..., description="Index of predicted class", examples=[0])
    face_detected: bool = Field(default=True, description="Whether a face was localized in the input", examples=[True])
    box: Optional[List[int]] = Field(default=None, description="Bounding box [x, y, w, h] of detected face, if found", examples=[[120, 80, 200, 200]])


class ErrorResponse(BaseModel):
    """Standard error detail response."""
    detail: str = Field(..., description="Error message explaining failure reason")


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.get(
    "/",
    summary="Root API Info",
    tags=["General"],
)
async def root():
    """Returns welcoming service information and links to documentation."""
    return {
        "service": "Face Mask Detection API (MobileNetV2)",
        "docs": "/docs",
        "demo": "/demo",
        "health": "/health",
        "model_loaded": detector.is_loaded,
    }


@app.get(
    "/demo",
    response_class=HTMLResponse,
    summary="Interactive Web Demo",
    tags=["Demo"],
)
async def web_demo():
    """Serves the interactive webcam and image upload demo UI."""
    return HTMLResponse(content=DEMO_HTML)


@app.get(
    "/samples/{filename}",
    summary="Get Sample Test Images",
    tags=["Demo"],
)
async def get_sample_image(filename: str):
    """Serve sample test images for evaluation and demo."""
    samples_dir = Path(__file__).resolve().parent / "samples"
    sample_path = (samples_dir / filename).resolve()
    if not sample_path.exists() or not str(sample_path).startswith(str(samples_dir)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sample image not found.",
        )
    return FileResponse(str(sample_path))


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check and Model Status",
    tags=["System"],
)
async def health_check():
    """Verify backend health and whether the trained MobileNetV2 model is loaded.

    Member 2's frontend can check this endpoint before initiating the webcam stream.
    """
    return HealthResponse(
        status="ok",
        model_loaded=detector.is_loaded,
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    responses={
        200: {"model": PredictionResponse, "description": "Successful prediction"},
        400: {"model": ErrorResponse, "description": "Invalid or unreadable image file"},
        503: {"model": ErrorResponse, "description": "Trained model not yet loaded"},
        500: {"model": ErrorResponse, "description": "Inference or server error"},
    },
    summary="Predict Face Mask from Uploaded Image",
    tags=["Inference"],
)
async def predict_mask(file: UploadFile = File(...)):
    """Receives an uploaded image frame from the React webcam interface and predicts mask status.

    - **file**: Multipart image file (JPEG, PNG, WebP).
    - Image is preprocessed with OpenCV and normalized for MobileNetV2.
    - Returns JSON containing predicted label and confidence score.
    """
    # 1. Validate file presence
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image file provided. Please upload a file with field name 'file'.",
        )

    # 2. Check if model is loaded before reading file
    if not detector.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Model is not loaded. Please ensure Member 1's trained model "
                "is placed at 'backend/model/mask_detector.keras'."
            ),
        )

    # 3. Read image bytes
    try:
        image_bytes = await file.read()
    except Exception as exc:
        logger.error("Failed to read uploaded file: %s", str(exc))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read uploaded file.",
        ) from exc

    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image file is empty.",
        )

    # 4. Perform prediction through detector service
    try:
        result = detector.predict(image_bytes)
        return PredictionResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            class_index=result["class_index"],
            face_detected=result.get("face_detected", False),
            box=result.get("box", None),
        )

    except InvalidImageError as exc:
        logger.warning("Invalid image upload: %s", str(exc))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except ModelNotLoadedError as exc:
        logger.error("Model not loaded error during prediction: %s", str(exc))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    except (PreprocessingError, PredictionError) as exc:
        logger.error("Prediction processing error: %s", str(exc), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the prediction.",
        ) from exc

    except Exception as exc:
        logger.error("Unexpected server error: %s", str(exc), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred.",
        ) from exc


# ---------------------------------------------------------------------------
# Direct Execution Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    logger.info("Starting Face Mask Detection API server on %s:%d", host, port)
    uvicorn.run("app:app", host=host, port=port, reload=True)
