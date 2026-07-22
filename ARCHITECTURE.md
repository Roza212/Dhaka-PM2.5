# System Architecture
## Hyper-Local Dhaka PM2.5 STGCN

### 1. High-Level Architecture

```mermaid
graph TD
    subgraph Data Sources
        OSM[OpenStreetMap]
        OAQ[OpenAQ Sensors]
        GMT[Google Maps Traffic APIs]
        WAPI[Weather APIs]
    end

    subgraph Data Engineering Pipeline
        ETL[Automated ETL Pipelines]
        GraphBuilder[Geospatial Graph Integrator]
    end

    subgraph ML & MLOps Ecosystem
        STGCN[STGCN Model]
        MLflow[MLflow Tracking]
        DVC[DVC Data Versioning]
    end

    subgraph Backend Services
        FastAPI[FastAPI REST APIs]
        Security[RBAC, Encryption, Audit Logs]
    end

    subgraph Presentation Layer
        Dashboard[GIS Predictive Dashboard]
        API_Consumers[Smart City Planners / Researchers]
    end

    OSM --> ETL
    OAQ --> ETL
    GMT --> ETL
    WAPI --> ETL

    ETL --> GraphBuilder
    GraphBuilder --> STGCN
    STGCN <--> MLflow
    STGCN <--> DVC

    STGCN --> FastAPI
    Security --> FastAPI

    FastAPI --> Dashboard
    FastAPI --> API_Consumers
```

### 2. Component Details
- **Geospatial Graph Integrator**: Fuses various data streams to form nodes (intersections) and edges (road segments with traffic speeds and wind vectors).
- **STGCN Model**: Uses the spatial graph and temporal data to predict pollution diffusion.
- **FastAPI Layer**: Secure, scalable interface connecting the predictive engine to end-user applications.
