# Kubernetes & CI/CD Deployment Guide

## 1. Local Docker Testing
Build and run the container locally:
```bash
docker build -t dhaka-pm25-backend .
docker run -p 8000:8000 --env JWT_SECRET_KEY="local-secret" dhaka-pm25-backend
```

## 2. Kubernetes Deployment
The production cluster utilizes 3 replicas. Apply the manifests:
```bash
kubectl apply -f infra/k8s/deployment.yaml
kubectl apply -f infra/k8s/service.yaml
```

## 3. CI/CD Workflow
The `.github/workflows/deploy.yml` automatically triggers on `main` branch pushes. It builds the Docker image, tags it with the Git SHA, and deploys it to the cluster.
