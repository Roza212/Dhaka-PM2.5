# Feature Engineering Specification
## Hyper-Local Dhaka PM2.5 STGCN

### 1. Overview
This document specifies the feature engineering methodology employed for the STGCN model. Proper feature selection and scaling are critical to ensure stable gradient descent and capture both spatial relationships (traffic, wind) and temporal patterns (time of day, seasonality).

### 2. Node Features
Nodes represent intersections or sensor locations.
- **Historical PM2.5 (Continuous)**: A rolling window of PM2.5 values (e.g., t, t-1, t-2). Scaled using `StandardScaler` to zero mean and unit variance.
- **Hour of Day (Cyclical)**: Extracted from the timestamp. Sine and Cosine transformations are applied to preserve the cyclical nature of time (23:00 is close to 00:00).
- **Day of Week (Cyclical)**: Encoded similarly with Sine and Cosine to capture weekend vs. weekday pollution patterns.
- **Temperature / Humidity (Continuous)**: Meteorological data attached to nodes, Min-Max scaled to [0, 1].

### 3. Edge Features
Edges represent physical road segments connecting nodes.
- **Traffic Bottleneck Weight (Continuous)**: Calculated as `1.0 / Traffic Speed`. High traffic congestion yields lower speed, thereby increasing the edge weight to simulate pollution accumulation.
- **Wind Vector Alignment (Continuous)**: A calculated dot product between the geographical vector of the edge and the wind direction vector. If the wind blows along the street, pollution propagates more strongly to the downstream node.

### 4. Selection Rationale
- **Why Cyclical Time?** Simple linear time (0-23) falsely implies a massive jump between hour 23 and hour 0. Sine/Cosine encoding resolves this.
- **Why Inverse Traffic Speed?** STGCN aggregates information from neighboring nodes via edge weights. Heavier weights imply stronger pollution propagation. Slower traffic means more idling engines and less dispersion.
- **Why Scaling?** Neural networks are highly sensitive to unscaled data. PM2.5 values (100-300) combined with bottleneck weights (0.01-0.1) would cause vanishing/exploding gradients. Standard scaling normalizes these distributions.
