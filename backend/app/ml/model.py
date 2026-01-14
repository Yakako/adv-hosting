"""
ML Model integration for car classification
"""
import tensorflow as tf
import numpy as np
import os
from app.core.config import settings

# Car classes - MUST match the order used during model training
CAR_CLASSES = [
    "Audi",
    "Hyundai Creta",
    "Mahindra Scorpio",
    "Rolls Royce",
    "Swift",
    "Tata Safari",
    "Toyota Innova"
]

# Load model
model = None

def load_model():
    """Load the ML model from disk"""
    global model
    try:
        if os.path.exists(settings.MODEL_PATH):
            model = tf.keras.models.load_model(settings.MODEL_PATH)
            print(f"✅ Model loaded successfully from {settings.MODEL_PATH}")
        else:
            print(f"⚠️  Model file not found: {settings.MODEL_PATH}")
            print("   Creating mock model for development...")
            model = create_mock_model()
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("   Creating mock model for development...")
        model = create_mock_model()

def create_mock_model():
    """Create a simple mock model for development/testing"""
    from tensorflow import keras
    from tensorflow.keras import layers
    
    mock_model = keras.Sequential([
        layers.Input(shape=(224, 224, 3)),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(len(CAR_CLASSES), activation='softmax')
    ])
    
    print("⚠️  Using UNTRAINED mock model - predictions will be random!")
    print("   Replace with trained model for production use.")
    return mock_model

def predict(input_data: np.ndarray) -> np.ndarray:
    """
    Make prediction on input image
    
    Args:
        input_data: numpy array of shape (1, 224, 224, 3)
        
    Returns:
        numpy array of prediction probabilities for each class
    """
    global model
    if model is None:
        load_model()
    
    if model is None:
        raise Exception("Model not loaded")
    
    prediction = model.predict(input_data, verbose=0)
    return prediction

# Load model on import
load_model()
