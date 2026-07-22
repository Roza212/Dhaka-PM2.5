# Hyper-Local Dhaka PM2.5 Dashboard User Guide

## Overview
This platform predicts hyper-local PM2.5 air pollution levels across Dhaka based on real-time traffic gridlock data and spatial-temporal graphs.

## Using the Dashboard
1. **Access**: Navigate to the public URL of the deployed frontend.
2. **Horizon Selection**: Use the dropdown in the sidebar to select your desired prediction horizon (`+1 Hour`, `+3 Hours`, `+6 Hours`).
3. **Live Sync**: Click "Live Sync Engine" to fetch the latest predictions.
4. **Visualization**:
    - The Map displays glowing markers at critical intersections. Cyan = Healthy, Orange = Unhealthy, Red = Severe Gridlock/Pollution.
    - The Chart dynamically visualizes the time-series PM2.5 curve.
