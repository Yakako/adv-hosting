from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
import os
import shutil
from pathlib import Path

from database.connection import init_db, get_db
from database.models import Prediction
from schemas.prediction import (
    PredictionResponse,
    PredictResponse,
    StatsResponse
)
from services.mock_model import get_model

# Create FastAPI app
app = FastAPI(
    title="Car Classification API",
    description="Backend API for car image classification",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed image extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("🚀 Starting Car Classification API...")
    init_db()
    print("✅ Application ready!")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Car Classification API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/hello")
async def hello():
    """Hello World endpoint"""
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": "Car Classification API",
        "version": "1.0.0"
    }


# ==================== PREDICTION API ROUTES ====================

@app.post("/api/predict", response_model=PredictResponse)
async def predict_car(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload car image and get prediction
    
    - **file**: Image file (JPG, PNG, etc.)
    
    Returns prediction with confidence score
    """
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = UPLOAD_DIR / filename
    
    try:
        # Save uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get model and make prediction
        model = get_model()
        result = model.predict(str(file_path))
        
        # Save prediction to database
        db_prediction = Prediction(
            image_path=str(file_path),
            predicted_class=result["predicted_class"],
            confidence=result["confidence"]
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        return PredictResponse(
            predicted_class=result["predicted_class"],
            confidence=result["confidence"],
            all_predictions=result["all_predictions"],
            prediction_id=db_prediction.id,
            image_path=str(file_path)
        )
        
    except Exception as e:
        # Clean up file if error occurs
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/api/predictions", response_model=List[PredictionResponse])
async def get_predictions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get prediction history
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    predictions = db.query(Prediction)\
        .order_by(Prediction.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return predictions


@app.get("/api/predictions/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    """
    Get single prediction by ID
    
    - **prediction_id**: ID of the prediction
    """
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    return prediction


@app.delete("/api/predictions/{prediction_id}")
async def delete_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a prediction
    
    - **prediction_id**: ID of the prediction to delete
    """
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    # Delete image file if exists
    if Path(prediction.image_path).exists():
        Path(prediction.image_path).unlink()
    
    db.delete(prediction)
    db.commit()
    
    return {"message": "Prediction deleted successfully", "id": prediction_id}


@app.get("/api/stats", response_model=StatsResponse)
async def get_statistics(db: Session = Depends(get_db)):
    """
    Get prediction statistics
    
    Returns total predictions, average confidence, most common class, etc.
    """
    # Total predictions
    total = db.query(func.count(Prediction.id)).scalar()
    
    if total == 0:
        return StatsResponse(
            total_predictions=0,
            average_confidence=0.0,
            most_common_class=None,
            predictions_today=0,
            class_distribution={}
        )
    
    # Average confidence
    avg_confidence = db.query(func.avg(Prediction.confidence)).scalar()
    
    # Most common class
    most_common = db.query(
        Prediction.predicted_class,
        func.count(Prediction.predicted_class).label('count')
    ).group_by(Prediction.predicted_class)\
     .order_by(func.count(Prediction.predicted_class).desc())\
     .first()
    
    # Predictions today
    today = datetime.now().date()
    predictions_today = db.query(func.count(Prediction.id))\
        .filter(func.date(Prediction.created_at) == today)\
        .scalar()
    
    # Class distribution
    class_dist = db.query(
        Prediction.predicted_class,
        func.count(Prediction.predicted_class).label('count')
    ).group_by(Prediction.predicted_class).all()
    
    class_distribution = {cls: count for cls, count in class_dist}
    
    return StatsResponse(
        total_predictions=total,
        average_confidence=float(avg_confidence) if avg_confidence else 0.0,
        most_common_class=most_common[0] if most_common else None,
        predictions_today=predictions_today,
        class_distribution=class_distribution
    )

