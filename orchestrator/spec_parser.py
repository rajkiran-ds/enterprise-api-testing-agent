"""Parse OpenAPI specs. Deterministic code only, no LLM."""


def load_spec(path: str) -> dict:
    """Load an OpenAPI JSON/YAML file and return it as a dict."""
    raise NotImplementedError


def extract_endpoints(spec: dict) -> list[dict]:
    """Return [{path, method, summary}] from spec['paths']."""
    raise NotImplementedError