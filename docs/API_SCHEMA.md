# Initial API Schema Definitions
## Hyper-Local Dhaka PM2.5 STGCN

This document outlines the core RESTful API endpoints and their associated JSON schemas, to be implemented via FastAPI.

### Base URL: `/api/v1`

---

### 1. Authentication
**POST** `/auth/token`
- **Purpose**: Authenticates a user and returns a JWT token.
- **Request Body**:
  ```json
  {
    "username": "admin",
    "password": "secure_password"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbG...",
    "token_type": "bearer"
  }
  ```

---

### 2. Predictions
**GET** `/predictions/hyperlocal`
- **Purpose**: Retrieves PM2.5 predictions for a specific geographic bounding box or intersection.
- **Query Parameters**:
  - `lat` (float): Latitude of the intersection.
  - `lng` (float): Longitude of the intersection.
  - `horizon` (int): Prediction horizon in hours (1, 3, or 6).
- **Headers**: `Authorization: Bearer <token>`
- **Response (200 OK)**:
  ```json
  {
    "intersection_id": "dhaka_shahbag_01",
    "coordinates": {"lat": 23.7383, "lng": 90.3957},
    "current_pm25": 145.2,
    "predictions": [
      {"hour_offset": 1, "predicted_pm25": 150.4},
      {"hour_offset": 3, "predicted_pm25": 162.1},
      {"hour_offset": 6, "predicted_pm25": 140.8}
    ],
    "confidence_score": 0.89,
    "model_version": "stgcn_v1.2"
  }
  ```

---

### 3. Graph System Status
**GET** `/graph/health`
- **Purpose**: Returns the health and data freshness of the underlying Spatial-Temporal Graph.
- **Headers**: `Authorization: Bearer <token>`
- **Response (200 OK)**:
  ```json
  {
    "status": "healthy",
    "total_nodes": 1024,
    "total_edges": 3056,
    "last_osm_sync": "2026-07-22T14:00:00Z",
    "last_traffic_update": "2026-07-22T14:10:00Z",
    "offline_sensors": 2
  }
  ```

---

### 4. Data Export
**GET** `/export/historical`
- **Purpose**: Exports historical actuals vs predictions for academic analysis.
- **Query Parameters**:
  - `start_date` (ISO 8601 string)
  - `end_date` (ISO 8601 string)
  - `format` (string): `csv` or `json`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200 OK)**: Returns the requested file blob.
