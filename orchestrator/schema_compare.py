"""Compare source and target API schemas. Deterministic code only."""


def find_missing_fields(source: dict, target: dict) -> list[str]:
    """Fields present in source but absent in target."""
    raise NotImplementedError


def find_breaking_changes(source: dict, target: dict) -> list[dict]:
    """Removed endpoints, changed types, newly required fields."""
    raise NotImplementedError