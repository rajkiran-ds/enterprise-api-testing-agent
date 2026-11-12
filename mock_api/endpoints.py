"""Planned endpoints for the mock enterprise API (Service 1, built in FastAPI on Day 5).

Each tuple is (method, path, description). See docs/API_DESIGN.md for details.
"""

PLANNED_ENDPOINTS: list[tuple[str, str, str]] = [
    ("GET", "/health", "service status"),
    ("GET", "/customers", "list customers"),
    ("POST", "/customers", "create customer, 422 on bad input"),
    ("GET", "/customers/{id}", "get customer, 404 if missing"),
    ("GET", "/orders", "list orders"),
    ("GET", "/simulate/error", "return an error on demand, e.g. ?code=500"),
]