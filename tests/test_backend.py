from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "user", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "user", "password": "wrongpassword"}
    )
    assert response.status_code == 400

def test_unauthorized_access():
    # Attempting to access predictions without a token
    response = client.get("/api/v1/predictions/hyperlocal?lat=23.8&lng=90.4&horizon=3")
    assert response.status_code == 401

def test_authorized_prediction():
    # 1. Login
    login_res = client.post(
        "/api/v1/auth/token",
        data={"username": "user", "password": "password"}
    )
    token = login_res.json()["access_token"]
    
    # 2. Request prediction with token
    res = client.get(
        "/api/v1/predictions/hyperlocal?lat=23.8&lng=90.4&horizon=3",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["current_pm25"] == 145.2
    assert "predictions" in data

def test_rbac_admin_only_route():
    # 1. Standard User login
    login_res = client.post(
        "/api/v1/auth/token",
        data={"username": "user", "password": "password"}
    )
    user_token = login_res.json()["access_token"]
    
    # Try accessing admin route -> Should be 403 Forbidden
    res = client.get("/api/v1/graph/health", headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 403 

    # 2. Admin login
    login_res = client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "secure_password"}
    )
    admin_token = login_res.json()["access_token"]
    
    # Try accessing admin route -> Should be 200 OK
    res = client.get("/api/v1/graph/health", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
