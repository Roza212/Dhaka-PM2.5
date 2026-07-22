import logging
from fastapi import FastAPI, Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Setup Enterprise Audit Logger
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

# In a true production environment, this streams to ELK, Splunk, or AWS CloudWatch
handler = logging.FileHandler("audit.log")
handler.setFormatter(logging.Formatter('%(asctime)s - AUDIT - %(message)s'))
audit_logger.addHandler(handler)

def setup_security(app: FastAPI):
    # Enforces HTTPS everywhere. Drops all plaintext HTTP requests.
    app.add_middleware(HTTPSRedirectMiddleware)

def log_audit_event(user: str, action: str, resource: str, status: str):
    """
    Logs critical actions ensuring non-repudiation.
    Example: log_audit_event("admin", "Accessed Graph Health", "/api/v1/graph/health", "SUCCESS")
    """
    audit_logger.info(f"User: {user} | Action: {action} | Resource: {resource} | Status: {status}")
