# Software Requirements Specification (SRS)
## Hyper-Local Dhaka PM2.5 STGCN

### 1. Introduction
This document specifies the software requirements for the Dhaka PM2.5 prediction platform.

### 2. Functional Requirements
- **FR1**: The system must ingest real-time data from OpenStreetMap, OpenAQ, Google Maps Traffic APIs, and Weather APIs.
- **FR2**: The system must convert the Dhaka road map into a mathematical graph (nodes and edges).
- **FR3**: The system must assign real-time traffic speeds to the graph edges dynamically.
- **FR4**: The STGCN model must generate PM2.5 predictions for specific intersections up to 6 hours in advance.
- **FR5**: The system must expose a GIS dashboard visualizing these predictions.
- **FR6**: The system must expose FastAPI REST endpoints for programmatic access to predictions.

### 3. Non-Functional Requirements
- **NFR1 (Performance)**: The ETL pipeline must process incoming data and update predictions within strict latency bounds suitable for real-time dashboards.
- **NFR2 (Security)**: All endpoints must be secured using RBAC, and sensitive data must be encrypted.
- **NFR3 (Reliability)**: The platform must log all activities for auditing and employ automated ML reproducibility tools (MLflow, DVC).
- **NFR4 (Scalability)**: The microservices architecture (FastAPI backend) must scale horizontally to handle increased data loads.
