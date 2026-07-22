# Project Roadmap
## Hyper-Local Dhaka PM2.5 STGCN

### Phase 1: Foundation & Data Integration
- Define system architecture and set up repositories.
- Implement automated ETL pipelines for OpenStreetMap, OpenAQ, Google Maps Traffic APIs, and Weather APIs.
- Construct the base geospatial graph of Dhaka's road network.

### Phase 2: ML Model Development
- Design and train the Spatial-Temporal Graph Convolutional Network (STGCN).
- Map real-time traffic speeds to graph edges.
- Integrate MLflow and DVC for experiment tracking and data versioning.
- Validate model performance against baseline time-series regression models.

### Phase 3: Backend & API Development
- Develop secure FastAPI REST APIs to serve predictions.
- Implement Role-Based Access Control (RBAC), encryption, and audit logging.
- Optimize inference latency for the STGCN model.

### Phase 4: Frontend GIS Dashboard & Production Deployment
- Develop the dynamic GIS mapping dashboard for real-time visualization.
- Deploy the end-to-end ecosystem to an enterprise-grade cloud environment.
- Prepare documentation and results for academic/smart city conference publication.
