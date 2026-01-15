"""
Tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_stats():
    """Test statistics endpoint"""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_predictions" in data
    assert "average_confidence" in data

def test_get_predictions():
    """Test get predictions endpoint"""
    response = client.get("/api/predictions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Add more tests as needed
