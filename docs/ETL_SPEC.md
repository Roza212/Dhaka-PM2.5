# ETL Pipeline Specification
## Hyper-Local Dhaka PM2.5 STGCN

### 1. Overview
This specification details the Extract, Transform, Load (ETL) pipeline responsible for ingesting real-time data from various environmental and traffic APIs to construct the spatio-temporal graph for Dhaka.

### 2. Extraction Sources
- **OpenAQ API**: Retrieves PM2.5 readings from active sensor nodes in Dhaka.
- **Google Maps Traffic API**: Retrieves current traffic speed (bottleneck data) for predefined road segments.
- **Weather API (e.g., OpenWeatherMap)**: Retrieves wind speed, direction, temperature, and humidity.
- **OpenStreetMap (OSM)**: Static ingestion of the base road graph (nodes/edges).

### 3. Transformation Logic
- **Data Cleaning**: Remove duplicate sensor readings and handle missing values (NaN imputation using historical averages or KNN).
- **Normalization**: Standardize timestamps to UTC. Scale continuous variables (e.g., PM2.5, wind speed) for neural network consumption.
- **Graph Assignment**: Map sensor data to specific graph nodes and traffic speeds to graph edges.

### 4. Load Strategy
- Transformed graph snapshots are stored as `.json` or `.parquet` files partitioned by timestamp in a local data lake (`/data/processed/`) for MLflow tracking and DVC versioning.

### 5. Error Handling & Retry
- All external API calls implement exponential backoff.
- Missing data beyond a tolerable threshold triggers alerts and halts the pipeline for manual review.
