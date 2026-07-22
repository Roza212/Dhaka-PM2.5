# Threat Model
## Hyper-Local Dhaka PM2.5 STGCN

This document outlines the primary threat model for our STGCN-based pollution prediction platform.

### 1. Asset Identification
- **External API Keys**: Google Maps Traffic API, OpenAQ API, Weather APIs.
- **Inference Infrastructure**: FastAPI endpoints serving the STGCN model predictions.
- **Data & Models**: Sensor data, generated spatio-temporal graphs, and the STGCN model weights.
- **User Data**: Authentication tokens (JWTs) and user profiles.

### 2. Identified Threats & Assumptions
1. **API Abuse & DDoS**: Public-facing FastAPI endpoints could be targeted by denial-of-service attacks or scraped aggressively, degrading performance for legitimate users.
2. **Credential Leakage**: Hardcoding or improperly storing `.env` files could expose premium API keys, leading to financial loss or quota exhaustion.
3. **Data Poisoning**: Ingesting compromised or manipulated sensor data from external APIs could skew the STGCN predictions.
4. **Unauthorized Access**: Weak JWT configurations or lack of RBAC could allow unprivileged users to access administrative MLops tools (MLflow/DVC) or sensitive model data.

### 3. Mitigations
- **Rate Limiting & Throttling**: Enforce strict IP-based and token-based rate limits on all FastAPI routes.
- **Environment Management**: Never commit `.env` files. Use strict secret management in production (e.g., AWS Secrets Manager or HashiCorp Vault).
- **Data Validation & Sanitization**: Implement rigorous schema validation (e.g., Pydantic) on all incoming data streams before feeding them into the graph builder.
- **Robust Authentication**: Use industry-standard JWTs with short expiration times, and implement strict Role-Based Access Control (RBAC) across all service boundaries.
- **Encryption**: Enforce TLS/SSL for all data in transit and encrypt data at rest where applicable.
