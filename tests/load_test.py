import time
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.main import app

client = TestClient(app)

def run_load_test():
    """
    Simulates a heavy load on the API to verify Rate Limiting and stability.
    """
    login_res = client.post("/api/v1/auth/token", data={"username": "user", "password": "password"})
    token = login_res.json()["access_token"]
    
    start_time = time.time()
    
    # Simulate burst of 120 concurrent requests 
    # (Exceeds the 100/min limit defined in backend/main.py)
    responses = []
    for _ in range(120):
        responses.append(
            client.get("/api/v1/predictions/hyperlocal?lat=23.8&lng=90.4&horizon=3", headers={"Authorization": f"Bearer {token}"})
        )
    
    end_time = time.time()
    
    successes = sum(1 for r in responses if r.status_code == 200)
    rate_limits = sum(1 for r in responses if r.status_code == 429)
    
    print(f"--- Load Test Results ---")
    print(f"Total Time: {end_time - start_time:.2f}s")
    print(f"Successful Requests (200): {successes}")
    print(f"Rate Limited Requests (429): {rate_limits}")
    
    # Assertions for CI/CD Pipeline
    assert successes <= 100, "Rate limiting middleware failed to throttle traffic."
    assert rate_limits > 0, "Rate limiting did not engage."

if __name__ == "__main__":
    run_load_test()
