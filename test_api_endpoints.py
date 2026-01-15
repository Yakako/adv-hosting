"""
Test API endpoints
"""
import requests
from io import BytesIO
from PIL import Image
import json

# API base URL
BASE_URL = "http://localhost:8001"

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer

def test_health_check():
    """Test health endpoint"""
    print("\n1️⃣ Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200
    print("   ✅ Health check passed!")

def test_predict():
    """Test prediction endpoint"""
    print("\n2️⃣ Testing /api/predict endpoint...")
    
    # Create test image
    image_buffer = create_test_image()
    
    files = {'file': ('test_car.jpg', image_buffer, 'image/jpeg')}
    response = requests.post(f"{BASE_URL}/api/predict", files=files)
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Predicted Class: {data['predicted_class']}")
    print(f"   Confidence: {data['confidence']:.2%}")
    print(f"   Prediction ID: {data['prediction_id']}")
    print(f"   Top 3 predictions:")
    for cls, conf in list(data['all_predictions'].items())[:3]:
        print(f"      - {cls}: {conf:.2%}")
    
    assert response.status_code == 200
    assert 'predicted_class' in data
    assert 'confidence' in data
    print("   ✅ Prediction test passed!")
    
    return data['prediction_id']

def test_get_predictions():
    """Test get predictions history"""
    print("\n3️⃣ Testing /api/predictions endpoint...")
    response = requests.get(f"{BASE_URL}/api/predictions")
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Total predictions found: {len(data)}")
    
    if data:
        print(f"   Latest prediction:")
        print(f"      - ID: {data[0]['id']}")
        print(f"      - Class: {data[0]['predicted_class']}")
        print(f"      - Confidence: {data[0]['confidence']:.2%}")
    
    assert response.status_code == 200
    assert isinstance(data, list)
    print("   ✅ Get predictions test passed!")

def test_get_prediction_by_id(prediction_id):
    """Test get single prediction"""
    print(f"\n4️⃣ Testing /api/predictions/{prediction_id} endpoint...")
    response = requests.get(f"{BASE_URL}/api/predictions/{prediction_id}")
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Prediction details:")
    print(f"      - ID: {data['id']}")
    print(f"      - Class: {data['predicted_class']}")
    print(f"      - Confidence: {data['confidence']:.2%}")
    print(f"      - Created: {data['created_at']}")
    
    assert response.status_code == 200
    assert data['id'] == prediction_id
    print("   ✅ Get prediction by ID test passed!")

def test_stats():
    """Test statistics endpoint"""
    print("\n5️⃣ Testing /api/stats endpoint...")
    response = requests.get(f"{BASE_URL}/api/stats")
    
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Statistics:")
    print(f"      - Total predictions: {data['total_predictions']}")
    print(f"      - Average confidence: {data['average_confidence']:.2%}")
    print(f"      - Most common class: {data['most_common_class']}")
    print(f"      - Predictions today: {data['predictions_today']}")
    print(f"      - Class distribution:")
    for cls, count in data['class_distribution'].items():
        print(f"         * {cls}: {count}")
    
    assert response.status_code == 200
    print("   ✅ Statistics test passed!")

def test_multiple_predictions():
    """Test multiple predictions"""
    print("\n6️⃣ Testing multiple predictions...")
    for i in range(3):
        image_buffer = create_test_image()
        files = {'file': (f'test_car_{i}.jpg', image_buffer, 'image/jpeg')}
        response = requests.post(f"{BASE_URL}/api/predict", files=files)
        print(f"   Prediction {i+1}: {response.json()['predicted_class']} ({response.json()['confidence']:.2%})")
    print("   ✅ Multiple predictions test passed!")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 TESTING CAR CLASSIFICATION API")
    print("=" * 60)
    
    try:
        test_health_check()
        prediction_id = test_predict()
        test_get_predictions()
        test_get_prediction_by_id(prediction_id)
        test_stats()
        test_multiple_predictions()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n📊 Summary:")
        print("   - Health check: ✅")
        print("   - Image upload & prediction: ✅")
        print("   - Get predictions: ✅")
        print("   - Get prediction by ID: ✅")
        print("   - Statistics: ✅")
        print("   - Multiple predictions: ✅")
        print("\n🎉 Your API is working perfectly!")
        print(f"\n📝 API Documentation: {BASE_URL}/docs")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
