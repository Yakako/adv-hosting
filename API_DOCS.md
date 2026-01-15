# 🚀 Quick Start Guide

## Installation

1. **Navigate to backend folder:**
```bash
cd backend
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment:**
```bash
cp .env.example .env
```

4. **Run the server:**
```bash
# Option 1: Using the run script
./run.sh

# Option 2: Direct uvicorn command
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### Base URL
```
http://localhost:8000
```

### Available Endpoints

#### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "app": "Car Classification API",
  "version": "1.0.0"
}
```

---

#### 2. Predict Car Class
```http
POST /api/predict
Content-Type: multipart/form-data
```

**Request:**
- `file`: Image file (JPG, PNG)

**Response:**
```json
{
  "class_name": "Audi",
  "confidence": 0.95,
  "all_predictions": {
    "Audi": 0.95,
    "Hyundai Creta": 0.02,
    "Mahindra Scorpio": 0.01,
    "Rolls Royce": 0.01,
    "Swift": 0.005,
    "Tata Safari": 0.003,
    "Toyota Innova": 0.002
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/predict \
  -F "file=@/path/to/car/image.jpg"
```

---

#### 3. Get Prediction History
```http
GET /api/predictions?skip=0&limit=100
```

**Response:**
```json
[
  {
    "id": 1,
    "image_path": "./uploads/20260114_123456_car.jpg",
    "predicted_class": "Audi",
    "confidence": 0.95,
    "created_at": "2026-01-14T12:34:56"
  }
]
```

---

#### 4. Get Single Prediction
```http
GET /api/predictions/{prediction_id}
```

**Response:**
```json
{
  "id": 1,
  "image_path": "./uploads/20260114_123456_car.jpg",
  "predicted_class": "Audi",
  "confidence": 0.95,
  "created_at": "2026-01-14T12:34:56"
}
```

---

#### 5. Get Statistics
```http
GET /api/stats
```

**Response:**
```json
{
  "total_predictions": 150,
  "most_predicted_class": "Swift",
  "average_confidence": 0.87,
  "predictions_by_class": {
    "Audi": 25,
    "Hyundai Creta": 20,
    "Mahindra Scorpio": 18,
    "Rolls Royce": 15,
    "Swift": 30,
    "Tata Safari": 22,
    "Toyota Innova": 20
  }
}
```

---

#### 6. Delete Prediction
```http
DELETE /api/predictions/{prediction_id}
```

**Response:**
```json
{
  "message": "Prediction deleted successfully"
}
```

---

## 🧪 Testing with Python

```python
import requests

# Upload and predict
url = "http://localhost:8000/api/predict"
files = {"file": open("car_image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())

# Get statistics
response = requests.get("http://localhost:8000/api/stats")
print(response.json())
```

## 🧪 Testing with JavaScript/Fetch

```javascript
// Upload and predict
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// Get statistics
fetch('http://localhost:8000/api/stats')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 📚 Interactive Documentation

Once the server is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔧 Configuration

Edit `.env` file to customize:

```env
APP_NAME="Car Classification API"
DEBUG=true
PORT=8000
DATABASE_URL=sqlite:///./car_classification.db
UPLOAD_DIR=./uploads
MODEL_PATH=app/ml/best_model.h5
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 🤝 For Team Members

### Model Team:
Place your trained model here:
```
backend/app/ml/best_model.h5
```

Model requirements:
- Input: `(batch, 224, 224, 3)` - RGB images
- Output: `(batch, 7)` - Softmax probabilities
- Classes: Audi, Hyundai Creta, Mahindra Scorpio, Rolls Royce, Swift, Tata Safari, Toyota Innova

### Frontend Team:
- Base URL: `http://localhost:8000`
- All endpoints return JSON
- CORS is enabled for development
- Use `/api/predict` for predictions
- Use `/api/stats` for dashboard data
