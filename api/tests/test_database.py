"""
Test database connection and models
"""
from database.connection import SessionLocal, init_db
from database.models import Prediction
from datetime import datetime

def test_database():
    """Test database operations"""
    
    # Initialize database
    print("🔧 Initializing database...")
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Create a test prediction
        print("\n➕ Creating test prediction...")
        test_prediction = Prediction(
            image_path="uploads/test_car.jpg",
            predicted_class="Audi",
            confidence=0.95
        )
        
        db.add(test_prediction)
        db.commit()
        db.refresh(test_prediction)
        
        print(f"✅ Created: {test_prediction}")
        
        # Query all predictions
        print("\n📊 Fetching all predictions...")
        predictions = db.query(Prediction).all()
        print(f"Found {len(predictions)} prediction(s):")
        for pred in predictions:
            print(f"  - ID: {pred.id}, Class: {pred.predicted_class}, Confidence: {pred.confidence:.2f}")
        
        # Query specific prediction
        print("\n🔍 Fetching prediction by ID...")
        pred = db.query(Prediction).filter(Prediction.id == test_prediction.id).first()
        print(f"Found: {pred.to_dict()}")
        
        # Clean up test data
        print("\n🧹 Cleaning up test data...")
        db.delete(test_prediction)
        db.commit()
        print("✅ Test data removed")
        
        print("\n✅ All database tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_database()
