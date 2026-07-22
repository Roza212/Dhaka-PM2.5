from pydantic import BaseModel
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    role: str

class PredictionRequest(BaseModel):
    lat: float
    lng: float
    horizon: int

class PredictionItem(BaseModel):
    hour_offset: int
    predicted_pm25: float

class PredictionResponse(BaseModel):
    intersection_id: str
    coordinates: dict
    current_pm25: float
    predictions: List[PredictionItem]
    confidence_score: float
    model_version: str
