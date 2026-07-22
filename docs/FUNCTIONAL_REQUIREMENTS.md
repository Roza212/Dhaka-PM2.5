# Exhaustive Functional Requirements
## Hyper-Local Dhaka PM2.5 STGCN

This document expands upon the baseline SRS to provide an exhaustive breakdown of functional capabilities required by the system, ensuring zero ambiguity during downstream development.

### 1. Data Ingestion Module (FR1)
- **1.1. OpenStreetMap (OSM) Sync**: A scheduled CRON job that pulls the latest bounding box for Dhaka, filtering for `highway` tags to define the road network.
- **1.2. OpenAQ Integration**: Polling OpenAQ nodes within Dhaka city limits every 15 minutes to retrieve the latest PM2.5 (ug/m3) values. Must handle API timeouts and rate-limit backoffs.
- **1.3. Google Maps Traffic Integration**: Polling specific major intersections every 5 minutes to capture real-time traffic speeds and gridlock status.
- **1.4. Weather APIs Integration**: Retrieving wind speed, wind direction, humidity, and temperature every 30 minutes, interpolating values for grid mapping.

### 2. Graph Construction & Transformation (FR2, FR3)
- **2.1. Node Definition**: Every major intersection and sensor location is defined as a graph Node, with geo-coordinates (Lat/Lng) serving as primary keys.
- **2.2. Edge Definition**: Connecting roads are defined as Edges.
- **2.3. Dynamic Edge Weighting**: Edges are continuously updated with inverse traffic speeds (slower traffic = higher weight/bottleneck) and directional wind vectors.
- **2.4. Data Sanitization**: If a sensor goes offline, the graph must impute the missing node data using spatial interpolation (K-Nearest Neighbors).

### 3. Predictive Engine (FR4)
- **3.1. Model Inference**: The PyTorch/TensorFlow STGCN model must consume the live graph data to predict PM2.5 values for the next 1, 3, and 6 hours.
- **3.2. Batch Processing**: Inference should run continuously on a 15-minute sliding window to provide real-time updates to the dashboard.
- **3.3. Fallback Mechanism**: If the STGCN inference fails, the system must fall back to a naive baseline (e.g., historical average) and flag the data quality in the API response.

### 4. API & Dashboard Services (FR5, FR6)
- **4.1. GIS Dashboard**: A map-based UI (e.g., Mapbox/Leaflet) rendering nodes (intersections) as color-coded heat dots (Green -> Red) representing predicted PM2.5 levels.
- **4.2. Secure Access**: All REST API endpoints serving prediction data must be protected via JWT authentication.
- **4.3. Data Export**: Researchers must be able to export historical prediction vs. actual data in CSV format for academic review.
