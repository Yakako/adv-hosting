"""
Pydantic schemas for prediction endpoints
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class PredictionResponse(BaseModel):
    """Response schema for prediction"""
    class_name: str
    confidence: float
    all_predictions: Dict[str, float]
    
    class Config:
        json_schema_extra = {
            "example": {
                "class_name": "Audi",
                "confidence": 0.95,
                "all_predictions": {
                    "Audi": 0.95,
                    "Swift": 0.03,
                    "Toyota Innova": 0.02
                }
            }
        }

class PredictionHistory(BaseModel):
    """Schema for prediction history"""
    id: int
    image_path: str
    predicted_class: str
    confidence: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    """Response schema for statistics"""
    total_predictions: int
    most_predicted_class: Optional[str]
    average_confidence: float
    predictions_by_class: Dict[str, int]
