"""
Mock Model Service for Testing
This simulates a car classification model
Replace this with your real model later
"""
import random
from typing import Dict

# Car classes that the model can predict
CAR_CLASSES = [
    "Audi",
    "BMW",
    "Mercedes-Benz",
    "Toyota",
    "Honda",
    "Tesla",
    "Ford",
    "Chevrolet",
    "Hyundai",
    "Nissan"
]


class MockCarClassifier:
    """
    Mock car classification model
    Returns random predictions for testing
    """
    
    def __init__(self):
        self.classes = CAR_CLASSES
        print("🤖 Mock model loaded")
    
    def predict(self, image_path: str) -> Dict[str, any]:
        """
        Simulate model prediction
        
        Args:
            image_path: Path to the uploaded image
            
        Returns:
            Dictionary with predicted_class and confidence
        """
        # Simulate model processing time
        # In real model, this is where you'd load and process the image
        
        # Generate random prediction
        predicted_class = random.choice(self.classes)
        confidence = random.uniform(0.75, 0.99)  # Random confidence between 75-99%
        
        # Generate probabilities for all classes
        all_predictions = {}
        remaining = 1.0 - confidence
        
        for cls in self.classes:
            if cls == predicted_class:
                all_predictions[cls] = confidence
            else:
                # Distribute remaining probability among other classes
                prob = random.uniform(0, remaining / len(self.classes))
                all_predictions[cls] = prob
        
        # Normalize to sum to 1.0
        total = sum(all_predictions.values())
        all_predictions = {k: v/total for k, v in all_predictions.items()}
        
        # Sort by confidence
        all_predictions = dict(sorted(all_predictions.items(), key=lambda x: x[1], reverse=True))
        
        return {
            "predicted_class": predicted_class,
            "confidence": all_predictions[predicted_class],
            "all_predictions": all_predictions
        }


# Global model instance
_model = None


def get_model() -> MockCarClassifier:
    """Get or create model instance"""
    global _model
    if _model is None:
        _model = MockCarClassifier()
    return _model
