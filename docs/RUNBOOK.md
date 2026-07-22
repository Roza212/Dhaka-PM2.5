# Operations Runbook

## Incident: HTTP 429 Too Many Requests (DDoS or Scraping)
- **Symptom**: Valid users report being unable to fetch predictions.
- **Cause**: The global rate limiter triggered (100 req/min threshold).
- **Resolution**: Investigate `audit.log` for malicious IPs. If load is legitimate, increase `RATE_LIMIT` in `backend/main.py`.

## Incident: Database Backup Failure
- **Symptom**: S3 bucket `dhaka-pm25-secure-backups` missing nightly dump.
- **Cause**: CRON failure, AES encryption key rotation failure, or IAM role denied.
- **Resolution**: Manually trigger `/infra/backup_script.sh` and observe `stdout` for exact openssl or aws-cli errors.

## Incident: Application Pods Crashing (OOM)
- **Symptom**: Kubernetes shows `OOMKilled` state on backend pods.
- **Cause**: Model loading into RAM exceeding `1Gi` limit.
- **Resolution**: Update `infra/k8s/deployment.yaml` resource limits to `2Gi` and re-apply.
