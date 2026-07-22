import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.main import app

client = TestClient(app)

def test_e2e_prediction_flow():
    """
    End-to-end integration test simulating a complete user journey.
    """
    # 1. User Authentication
    login_res = client.post("/api/v1/auth/token", data={"username": "user", "password": "password"})
    assert login_res.status_code == 200, "E2E: Login failed"
    token = login_res.json()["access_token"]
    
    # 2. Authenticated Data Request
    res = client.get(
        "/api/v1/predictions/hyperlocal?lat=23.8&lng=90.4&horizon=3", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200, "E2E: Prediction request rejected"
    
    # 3. Payload Validation
    data = res.json()
    assert "predictions" in data
    assert len(data["predictions"]) > 0
    assert "current_pm25" in data
