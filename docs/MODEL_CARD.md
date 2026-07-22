# STGCN Model Card

## Model Details
- **Architecture**: Spatial-Temporal Graph Convolutional Network (STGCN)
- **Framework**: PyTorch
- **Version**: 1.0.0

## Intended Use
Designed to forecast short-term (1-6 hours) localized PM2.5 spikes in Dhaka by correlating real-time traffic speeds with sensor data across a directed graph topology.

## Evaluation
- **Metrics Evaluated**: Root Mean Squared Error (RMSE), Mean Absolute Error (MAE).
- **Validation Constraints**: Forward pass tensors are strictly asserted to return finite floats (no `NaN` or `Infinity` propagation).

## Limitations
- Model performance drops significantly if OpenAQ sensors go offline.
- Extremely severe, unpredicted weather events (cyclones) degrade short-term horizon accuracy.
