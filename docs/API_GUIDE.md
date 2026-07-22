# FastAPI Documentation & API Guide

## Base URL
`/api/v1`

## Authentication
All endpoints (except login) require a standard OAuth2 `Bearer` JWT token.

### 1. `POST /auth/token`
Generates a JWT access token.
- **Form Data**: `username`, `password`
- **Returns**: `access_token`, `token_type`

### 2. `GET /predictions/hyperlocal`
Fetches the STGCN predictions.
- **Query Params**: `lat` (float), `lng` (float), `horizon` (int)
- **Returns**: JSON object containing current PM2.5, AI confidence, and an array of `PredictionItem`.

### 3. `GET /graph/health` (Admin Only)
Fetches topology health.
- **RBAC**: Requires the `admin` role in the JWT payload.
- **Returns**: Node and Edge counts, offline sensor states.
