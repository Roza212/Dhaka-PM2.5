import os
import sys
import pytest
import pandas as pd

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.etl_pipeline import ETLPipeline

def test_extract_air_quality():
    pipeline = ETLPipeline()
    data = pipeline.extract_air_quality()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "location" in data[0]
    assert "value" in data[0]

def test_transform_data():
    pipeline = ETLPipeline()
    raw_mock = [
        {"location": "Loc1", "value": 100.0, "lastUpdated": "2026-07-22T14:00:00Z"},
        {"location": "Loc2", "value": None, "lastUpdated": "2026-07-22T14:00:00Z"}
    ]
    df = pipeline.transform_data(raw_mock)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    # Check if NaN was imputed (mean of 100 is 100)
    assert df.iloc[1]['value'] == 100.0
    # Check datetime conversion
    assert pd.api.types.is_datetime64_any_dtype(df['lastUpdated'])
