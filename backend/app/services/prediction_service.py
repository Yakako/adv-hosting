"""
Prediction service - handles business logic for predictions
"""
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from PIL import Image
import numpy as np
import io
import os
import json
from datetime import datetime

from app.models.prediction import Prediction
from app.ml.model import predict, CAR_CLASSES
from app.core.config import settings

class PredictionService:
    """Service for handling predictions"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def predict(self, file: UploadFile):
        """
        Process image and make prediction
        
        Args:
            file: Uploaded image file
            
        Returns:
            Prediction result with class and confidence
        """
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and preprocess image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save uploaded image
        image_path = await self._save_image(file, contents)
        
        # Preprocess for model
        image_array = self._preprocess_image(image)
        
        # Get prediction from model
        prediction = predict(image_array)
        
        # Process results
        class_idx = np.argmax(prediction[0])
        confidence = float(prediction[0][class_idx])
        predicted_class = CAR_CLASSES[class_idx]
        
        all_predictions = {
            CAR_CLASSES[i]: float(prediction[0][i]) 
            for i in range(len(CAR_CLASSES))
        }
        
        # Save to database
        db_prediction = Prediction(
            image_path=image_path,
            predicted_class=predicted_class,
            confidence=confidence,
            all_predictions=json.dumps(all_predictions)
        )
        self.db.add(db_prediction)
        self.db.commit()
        self.db.refresh(db_prediction)
        
        return {
            "class_name": predicted_class,
            "confidence": confidence,
            "all_predictions": all_predictions
        }
    
    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for model input"""
        # Resize to model input size
        image = image.resize((224, 224))
        
        # Convert to array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    
    async def _save_image(self, file: UploadFile, contents: bytes) -> str:
        """Save uploaded image to disk"""
        # Create uploads directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Save file
        with open(filepath, "wb") as f:
            f.write(contents)
        
        return filepath
