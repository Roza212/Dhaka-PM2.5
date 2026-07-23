import pytest
from passlib.context import CryptContext
from unittest.mock import patch, MagicMock

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_password_hashing():
    password = "supersecretpassword123!"
    hashed = pwd_context.hash(password)
    
    assert password != hashed
    assert pwd_context.verify(password, hashed) is True
    assert pwd_context.verify("wrongpassword", hashed) is False

@patch('backend.main.redis_client')
@patch('backend.main.REDIS_AVAILABLE', True)
def test_redis_cache_hit(mock_redis):
    from backend.main import get_hyperlocal_predictions
    from sqlalchemy.orm import Session
    import json
    
    # Mock a cache hit
    mock_redis.get.return_value = json.dumps({"cached": "true", "current_pm25": 100})
    
    # Dummy DB session
    mock_db = MagicMock(spec=Session)
    
    response = get_hyperlocal_predictions(lat=23.8, lng=90.4, horizon=3, db=mock_db)
    
    assert response.status_code == 200
    assert json.loads(response.body)["cached"] == "true"
    mock_redis.get.assert_called_once_with("pred:23.8:90.4:3")
