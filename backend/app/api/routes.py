"""
API routes for car classification
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import json

from app.models.database import get_db
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionResponse, PredictionHistory, StatsResponse
from app.services.prediction_service import PredictionService

api_router = APIRouter()

@api_router.post("/predict", response_model=PredictionResponse)
async def predict_car(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a car image and get prediction
    
    - **file**: Image file (JPG, PNG)
    - Returns predicted car class with confidence scores
    """
    try:
        service = PredictionService(db)
        result = await service.predict(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@api_router.get("/predictions", response_model=List[PredictionHistory])
async def get_predictions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get prediction history
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    predictions = db.query(Prediction).offset(skip).limit(limit).all()
    return predictions

@api_router.get("/predictions/{prediction_id}", response_model=PredictionHistory)
async def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """Get a specific prediction by ID"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

@api_router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """
    Get statistics about predictions
    
    Returns total predictions, most predicted class, and distribution
    """
    predictions = db.query(Prediction).all()
    
    if not predictions:
        return StatsResponse(
            total_predictions=0,
            most_predicted_class=None,
            average_confidence=0.0,
            predictions_by_class={}
        )
    
    # Calculate statistics
    total = len(predictions)
    avg_confidence = sum(p.confidence for p in predictions) / total
    
    # Count predictions by class
    class_counts = {}
    for p in predictions:
        class_counts[p.predicted_class] = class_counts.get(p.predicted_class, 0) + 1
    
    most_predicted = max(class_counts, key=class_counts.get)
    
    return StatsResponse(
        total_predictions=total,
        most_predicted_class=most_predicted,
        average_confidence=avg_confidence,
        predictions_by_class=class_counts
    )

@api_router.delete("/predictions/{prediction_id}")
async def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """Delete a prediction by ID"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    db.delete(prediction)
    db.commit()
    return {"message": "Prediction deleted successfully"}
