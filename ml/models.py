import torch
import torch.nn as nn
import torch.nn.functional as F

class BaselineModel(nn.Module):
    def __init__(self, input_dim: int, output_dim: int):
        super(BaselineModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.out = nn.Linear(32, output_dim)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x)

class STGCNModel(nn.Module):
    """
    Spatio-Temporal Graph Convolutional Network Architecture.
    Simulates graph processing and temporal sequence modeling.
    """
    def __init__(self, num_nodes: int, num_features: int, output_dim: int):
        super(STGCNModel, self).__init__()
        # Ensure we capture num_nodes structurally
        self.num_nodes = num_nodes
        
        # Temporal convolution captures sequence data across time
        self.temporal_conv = nn.Conv1d(in_channels=num_features, out_channels=32, kernel_size=3, padding=1)
        
        # Spatial convolution simulates message passing between graph nodes
        self.spatial_linear = nn.Linear(32, 64) 
        
        # Output prediction layer
        self.output_layer = nn.Linear(64, output_dim)
        
    def forward(self, x, edge_index, edge_weight=None):
        # Expected x shape: [batch_size, num_nodes, num_features, seq_length]
        # Example: [1, 100, 5, 12]
        batch_size, num_nodes, num_features, seq_length = x.size()
        
        # Flatten batch and nodes for temporal conv
        # Shape becomes: [batch_size * num_nodes, num_features, seq_length]
        x = x.view(batch_size * num_nodes, num_features, seq_length)
        
        # 1. Temporal Gated Convolution
        x = F.relu(self.temporal_conv(x))
        
        # 2. Spatial Aggregation (Simplified simulation of GCN)
        # Flattening temporal dimension to feed spatial
        x = torch.mean(x, dim=2) 
        x = F.relu(self.spatial_linear(x))
        
        # Average across nodes for a single global prediction (simplified)
        x = x.view(batch_size, num_nodes, -1)
        x = torch.mean(x, dim=1)
        
        # 3. Output prediction (e.g., predicting PM2.5 at t+1)
        return self.output_layer(x)
