"""Planned endpoints for the mock enterprise API (built in FastAPI on Day 5)."""

PLANNED_ENDPOINTS: list[tuple[str, str, str]] = [
    ("GET", "/health", "service status"),
    ("GET", "/customers", "list customers"),
    ("POST", "/customers", "create customer, 422 on bad input"),
    ("GET", "/customers/{id}", "404 if missing"),
    ("GET", "/simulate/error", "return a 500 on demand"),
]