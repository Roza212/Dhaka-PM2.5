import os
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml.feature_engineering import FeatureEngineer

def test_cyclical_encoding():
    engineer = FeatureEngineer()
    df = pd.DataFrame({'hour': [0, 6, 12, 18, 24]})
    df = engineer.add_cyclical_features(df, 'hour', 24.0)
    
    # Hour 0 and Hour 24 should have the exact same encoding
    assert np.isclose(df.loc[0, 'hour_sin'], df.loc[4, 'hour_sin'])
    assert np.isclose(df.loc[0, 'hour_cos'], df.loc[4, 'hour_cos'])
    
    # Hour 12 should be opposite of hour 0 in cosine
    assert np.isclose(df.loc[2, 'hour_cos'], -1.0)

def test_node_feature_scaling():
    engineer = FeatureEngineer()
    train_data = pd.DataFrame({
        'timestamp': ['2026-07-22T00:00:00Z', '2026-07-22T12:00:00Z'],
        'pm25': [50.0, 150.0],
        'temperature': [25.0, 35.0]
    })
    
    processed_train = engineer.fit_transform_node_features(train_data)
    
    # Scaler mean should be 100
    assert np.isclose(engineer.pm25_scaler.mean_[0], 100.0)
    # Min-Max scaled temp should be bounded between 0 and 1
    assert processed_train['temperature'].min() == 0.0
    assert processed_train['temperature'].max() == 1.0

def test_edge_feature_processing():
    engineer = FeatureEngineer()
    edges = pd.DataFrame({'traffic_speed': [10.0, 50.0, 0.0]})
    processed_edges = engineer.process_edge_features(edges)
    
    # Slower traffic -> higher weight
    assert processed_edges.loc[0, 'bottleneck_weight'] > processed_edges.loc[1, 'bottleneck_weight']
    # Zero traffic handled safely
    assert processed_edges.loc[2, 'bottleneck_weight'] == 10.0 # 1.0 / 0.1
