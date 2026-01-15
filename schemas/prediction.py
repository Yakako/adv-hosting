"""
Pydantic schemas for prediction API
"""
from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime


class PredictionResponse(BaseModel):
    """Response for single prediction"""
    id: int
    image_path: str
    predicted_class: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    created_at: datetime
    
    class Config:
        from_attributes = True


class PredictionCreate(BaseModel):
    """Schema for creating a prediction"""
    image_path: str
    predicted_class: str
    confidence: float


class PredictResponse(BaseModel):
    """Response for prediction endpoint"""
    predicted_class: str
    confidence: float
    all_predictions: Dict[str, float]
    prediction_id: int
    image_path: str
    message: str = "Prediction successful"


class StatsResponse(BaseModel):
    """Response for statistics endpoint"""
    total_predictions: int
    average_confidence: float
    most_common_class: Optional[str] = None
    predictions_today: int
    class_distribution: Dict[str, int]
