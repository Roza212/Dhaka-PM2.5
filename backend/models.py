from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
from datetime import datetime

class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")

class PM25Reading(Base):
    __tablename__ = "pm25_readings"
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float, index=True)
    lng = Column(Float, index=True)
    pm25_value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
