import torch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml.models import STGCNModel

def test_model_output_bounds():
    """
    Validates model output to ensure predictions are numerically stable.
    """
    model = STGCNModel(num_nodes=100, num_features=5, output_dim=1)
    
    # Simulating a chaotic batch of input data
    x = torch.randn(10, 5, 12) * 100 
    edge_index = torch.tensor([[0, 1], [1, 0]], dtype=torch.long)
    
    out = model(x, edge_index)
    
    # Assert dimensions
    assert out.shape == (10, 1), "Output shape mismatch"
    
    # Assert numerical stability (no exploding gradients resulting in NaN/Inf)
    assert torch.all(torch.isfinite(out)), "Model output contains NaN or Infinity values"
