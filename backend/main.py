from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Dict
import time

from . import schemas, auth

app = FastAPI(title="Hyper-Local Dhaka PM2.5 API")

# Simple In-Memory Rate Limiting
rate_limit_records: Dict[str, list] = {}
RATE_LIMIT = 100 # requests per minute

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    
    if client_ip not in rate_limit_records:
        rate_limit_records[client_ip] = []
    
    # Clean up old requests
    rate_limit_records[client_ip] = [t for t in rate_limit_records[client_ip] if now - t < 60]
    
    if len(rate_limit_records[client_ip]) >= RATE_LIMIT:
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        
    rate_limit_records[client_ip].append(now)
    response = await call_next(request)
    return response

@app.post("/api/v1/auth/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Mock user database
    if form_data.username == "admin" and form_data.password == "secure_password":
        access_token = auth.create_access_token(data={"sub": form_data.username, "role": "admin"})
        return {"access_token": access_token, "token_type": "bearer"}
    elif form_data.username == "user" and form_data.password == "password":
        access_token = auth.create_access_token(data={"sub": form_data.username, "role": "user"})
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect username or password"
    )

@app.get("/api/v1/predictions/hyperlocal", response_model=schemas.PredictionResponse)
async def get_hyperlocal_predictions(
    lat: float, 
    lng: float, 
    horizon: int, 
    current_user: dict = Depends(auth.get_current_user)
):
    # This route requires a valid JWT but is accessible by any authenticated user
    predictions = [
        schemas.PredictionItem(hour_offset=1, predicted_pm25=150.4),
        schemas.PredictionItem(hour_offset=horizon, predicted_pm25=140.8)
    ]
    return schemas.PredictionResponse(
        intersection_id=f"dhaka_mock_{lat}_{lng}",
        coordinates={"lat": lat, "lng": lng},
        current_pm25=145.2,
        predictions=predictions,
        confidence_score=0.89,
        model_version="stgcn_v1.2"
    )

@app.get("/api/v1/graph/health")
async def get_graph_health(current_user: dict = Depends(auth.require_admin)):
    # This route requires a valid JWT AND the user role must be 'admin'
    return {
        "status": "healthy",
        "total_nodes": 1024,
        "total_edges": 3056,
        "offline_sensors": 2
    }
