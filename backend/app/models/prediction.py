"""
Database models for predictions
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.models.database import Base

class Prediction(Base):
    """Prediction model to store prediction history"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=False)
    predicted_class = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    all_predictions = Column(String)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Prediction {self.id}: {self.predicted_class} ({self.confidence:.2%})>"
