# Data Card

## Provenance
- **OpenStreetMap (OSM)**: Used for generating the baseline spatial road graph and intersection nodes.
- **OpenAQ**: Historical and real-time PM2.5 environmental sensor data.
- **Google Maps Traffic**: Inverse-mapped traffic speeds converted into dynamic edge weights.

## Preprocessing (ETL)
- **Imputation**: Missing PM2.5 values are dynamically imputed using K-Nearest Neighbors (KNN).
- **Encoding**: Temporal features (Hour of Day, Day of Week) are transformed using Sine/Cosine cyclic encoding to preserve continuity across midnight boundary conditions.
- **Scaling**: All features are bound using Scikit-Learn `MinMaxScaler` and `StandardScaler`.

## Ethics & Privacy
- **PII**: No Personally Identifiable Information (PII) is collected, stored, or processed.
- **Bias**: The dataset represents environmental and geographic data universally.
