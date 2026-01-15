"""
Database models for the application
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .connection import Base


class Prediction(Base):
    """
    Prediction model - stores car classification predictions
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image_path = Column(String, nullable=False)  # Path to uploaded image
    predicted_class = Column(String, nullable=False)  # e.g., "Audi", "BMW"
    confidence = Column(Float, nullable=False)  # Prediction confidence (0-1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Prediction(id={self.id}, class={self.predicted_class}, confidence={self.confidence:.2f})>"

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "image_path": self.image_path,
            "predicted_class": self.predicted_class,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
