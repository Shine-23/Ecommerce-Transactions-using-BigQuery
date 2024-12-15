metrics = {
    "primary_requests": 0,
    "backup_requests": 0,
    "primary_status": True,  # Assume the primary backend is online initially
    "active_service": "primary"  # Track which service is active
}

def log_request(service):
    if service == "primary":
        metrics["primary_requests"] += 1
    elif service == "backup":
        metrics["backup_requests"] += 1
        metrics["active_service"] = "backup"

def set_primary_status(status):
    metrics["primary_status"] = status
    # If the primary is down, mark the backup as active
    if not status:
        metrics["active_service"] = "backup"

# Get metrics for visualization
def get_metrics():
    return metrics
