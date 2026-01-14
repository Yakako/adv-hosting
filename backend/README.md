# Car Classification Backend API

A FastAPI-based backend for car image classification using deep learning.

## 🚀 Features

- **Image Upload & Prediction** - Upload car images and get AI predictions
- **RESTful API** - Clean, well-documented endpoints
- **Database Integration** - Track predictions and user data
- **CORS Enabled** - Ready for frontend integration
- **Docker Support** - Easy deployment
- **Auto-reload** - Development mode with hot reload

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Configuration & settings
│   ├── models/        # Database models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── ml/            # ML model integration
├── uploads/           # Uploaded images storage
├── tests/             # Unit tests
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker configuration
└── .env.example       # Environment variables template
```

## 🛠️ Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔌 API Endpoints

### Health Check
```
GET /health
```

### Car Prediction
```
POST /api/predict
Content-Type: multipart/form-data
Body: file (image file)

Response:
{
  "class": "Audi",
  "confidence": 0.95,
  "all_predictions": {...}
}
```

### Prediction History
```
GET /api/predictions
GET /api/predictions/{id}
```

### Statistics
```
GET /api/stats
```

## 🤝 Team Integration

### For Model Team:
Place your trained model file here:
```
backend/app/ml/best_model.h5
```

Model requirements:
- Input shape: `(None, 224, 224, 3)`
- Output shape: `(None, 7)` - 7 car classes
- Classes order: Audi, Hyundai Creta, Mahindra Scorpio, Rolls Royce, Swift, Tata Safari, Toyota Innova

### For Frontend Team:
- Base URL: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- CORS enabled for all origins in development

## 🐳 Docker Deployment

```bash
docker build -t car-backend .
docker run -p 8000:8000 car-backend
```

## 🧪 Testing

```bash
pytest tests/
```

## 📝 Environment Variables

- `DATABASE_URL` - Database connection string
- `UPLOAD_DIR` - Directory for uploaded images
- `MODEL_PATH` - Path to ML model file
- `CORS_ORIGINS` - Allowed CORS origins
- `DEBUG` - Debug mode (true/false)

## 👥 Team Members

- Backend: [Your Name]
- Frontend: [Frontend Team]
- Model: [Model Team]

## 📄 License

MIT
