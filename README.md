# Car Classification Backend API

A FastAPI-based backend service for car image classification.

## 📋 Project Structure

```
backend/
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker container configuration
├── docker-compose.yml      # Docker Compose setup (PostgreSQL)
├── run.sh                  # Quick start script
├── API_DOCS.md             # Detailed API documentation
├── BACKEND_SUMMARY.md      # Backend summary
├── database/
│   └── connection.py       # Database connection utilities
├── tests/
│   └── test_api.py        # API endpoint tests
└── uploads/                # Directory for uploaded images
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip package manager
- PostgreSQL (optional, for database features)

### Installation

1. **Navigate to backend folder:**
```bash
cd backend
```

2. **Create virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Running the Application

**Option 1: Using the run script**
```bash
chmod +x run.sh
./run.sh
```

**Option 2: Direct uvicorn command**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at: **http://localhost:8000**

## 📡 API Endpoints

### Current Endpoints

#### Hello World
```
GET /hello
```

**Response:**
```json
{
  "message": "Hello World"
}
```

### Interactive Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

For planned API endpoints and features, see [API_DOCS.md](API_DOCS.md)

## 🐳 Docker Setup

### Run PostgreSQL Database

Start the PostgreSQL database with Docker Compose:
```bash
docker-compose up -d
```

Database configuration:
- **Host:** localhost
- **Port:** 5432
- **Database:** car_classification
- **User:** car_user
- **Password:** car_password

### Build and Run Backend Container

```bash
# Build the image
docker build -t car-classification-backend .

# Run the container
docker run -p 8000:8000 car-classification-backend
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

Run specific test:
```bash
pytest tests/test_api.py::test_health_check -v
```

## 📦 Dependencies

Main dependencies:
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - Lightning-fast ASGI server
- **Pydantic** - Data validation using Python type hints
- **pytest** - Testing framework

See [requirements.txt](requirements.txt) for complete list with versions.

## 🔧 Development

### Project Status

Current implementation:
- ✅ Basic FastAPI application setup
- ✅ Hello World endpoint
- ✅ Docker configuration
- ✅ PostgreSQL database setup
- ✅ Test structure
- ⏳ Car classification endpoints (planned)
- ⏳ Database models (planned)
- ⏳ ML model integration (planned)

### Adding New Endpoints

1. Open `main.py`
2. Add your route handler:
```python
@app.get("/your-endpoint")
async def your_function():
    return {"data": "value"}
```
3. Add tests in `tests/test_api.py`
4. Run tests to verify

### Development Mode

The application runs with auto-reload enabled for development. Any changes to Python files will automatically restart the server.

## 📝 Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Database
DATABASE_URL=postgresql://car_user:car_password@localhost:5432/car_classification

# Application
DEBUG=true
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760  # 10MB

# CORS (add your frontend URL)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🗄️ Database

PostgreSQL database is configured via Docker Compose. The connection parameters are:

```
Host: localhost
Port: 5432
Database: car_classification
Username: car_user
Password: car_password
```

To connect:
```bash
# Using psql
psql -h localhost -U car_user -d car_classification

# Connection string
postgresql://car_user:car_password@localhost:5432/car_classification
```

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# View database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove and recreate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is part of an Advanced Programming for Data Science course project.

---

**Project:** Car Classification Backend  
**Course:** Advanced Programming for DS  
**Date:** January 2026
