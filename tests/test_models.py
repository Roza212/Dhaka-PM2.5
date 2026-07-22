import os
import sys
import torch
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml.models import BaselineModel, STGCNModel

def test_baseline_forward():
    model = BaselineModel(input_dim=10, output_dim=1)
    x = torch.randn(32, 10) # Batch size 32, 10 features
    
    out = model(x)
    assert out.shape == (32, 1), "Baseline forward pass failed dimensional check."
    assert not torch.isnan(out).any(), "NaN found in baseline output."

def test_stgcn_forward():
    model = STGCNModel(num_nodes=100, num_features=5, output_dim=1)
    # [batch_size, num_features, seq_length]
    x = torch.randn(32, 5, 12) 
    
    # Mock edges (2 connections)
    edge_index = torch.tensor([[0, 1], [1, 0]], dtype=torch.long)
    
    out = model(x, edge_index)
    assert out.shape == (32, 1), "STGCN forward pass failed dimensional check."
    assert not torch.isnan(out).any(), "NaN found in STGCN output."
