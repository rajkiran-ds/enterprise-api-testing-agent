"""Parse OpenAPI 3 JSON/YAML into APISpec objects. Deterministic code only, no LLM."""
import json
import logging
import sys
from pathlib import Path

import yaml

from orchestrator.models import APISpec, DuplicateEndpointError, Endpoint, Schema, SpecParseError

log = logging.getLogger(__name__)
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}


def load_spec(path: str | Path) -> dict:
    """Read a .json/.yaml/.yml file and return the raw dict."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Spec not found: {p}")
    ext = p.suffix.lower()
    if ext not in {".json", ".yaml", ".yml"}:
        raise SpecParseError(f"Unsupported spec type '{ext}'. Use .json, .yaml or .yml")
    text = p.read_text(encoding="utf-8")
    try:
        data = json.loads(text) if ext == ".json" else yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise SpecParseError(f"Invalid {ext} in {p.name}: {exc}") from exc
    if not isinstance(data, dict):
        raise SpecParseError(f"{p.name} must contain an object at the top level")
    return data


def _resolve(raw: dict, node: dict, name: str = "") -> tuple[dict, str]:
    """Follow $ref pointers like '#/components/schemas/Customer'."""
    hops = 0
    while isinstance(node, dict) and "$ref" in node:
        ref = node["$ref"]
        name = ref.rsplit("/", 1)[-1]
        target = raw
        for part in ref.lstrip("#/").split("/"):
            try:
                target = target[part]
            except (KeyError, TypeError) as exc:
                raise SpecParseError(f"Broken $ref: {ref}") from exc
        node = target
        hops += 1
        if hops > 10:
            raise SpecParseError(f"$ref chain too deep at {ref}")
    return node, name


def _to_schema(raw: dict, node: dict, default_name: str) -> Schema:
    node, name = _resolve(raw, node, default_name)
    if node.get("type") == "array":
        node, name = _resolve(raw, node.get("items", {}), name)
    fields = {}
    for field, sub in node.get("properties", {}).items():
        sub, _ = _resolve(raw, sub)
        fields[field] = sub.get("type", "object")
    return Schema(name or default_name, fields, node.get("required", []))


def _success_schema(raw: dict, operation: dict, label: str) -> Schema | None:
    responses = operation.get("responses", {})
    for code in sorted(responses, key=str):
        if str(code).startswith("2"):
            resp, _ = _resolve(raw, responses[code])
            schema = resp.get("content", {}).get("application/json", {}).get("schema")
            if schema:
                return _to_schema(raw, schema, label)
    return None


def parse_spec(raw: dict) -> APISpec:
    """Turn a raw OpenAPI dict into an APISpec."""
    paths = raw.get("paths")
    if not isinstance(paths, dict):
        raise SpecParseError("Spec has no 'paths' section")
    info = raw.get("info", {})
    spec = APISpec(info.get("title", "Untitled"), str(info.get("version", "0")))
    for path, item in paths.items():
        for method, operation in item.items():
            if method.lower() not in HTTP_METHODS:
                continue  # skip 'parameters', 'summary' etc.
            response = _success_schema(raw, operation, f"{method.upper()} {path}")
            spec.add_endpoint(Endpoint(method, path, operation.get("summary", ""), response))
    log.info("Parsed %s v%s: %d endpoints", spec.title, spec.version, len(spec.endpoints))
    return spec


def extract_endpoints(raw: dict) -> list[dict]:
    """Return [{path, method, summary}] for every endpoint."""
    return [
        {"path": e.path, "method": e.method, "summary": e.summary}
        for e in parse_spec(raw).endpoints.values()
    ]


if __name__ == "__main__":
    from orchestrator import config
    config.setup_logging()
    if len(sys.argv) < 2:
        print("Usage: python -m orchestrator.spec_parser <spec.json|spec.yaml>", file=sys.stderr)
        sys.exit(1)
    try:
        s = parse_spec(load_spec(sys.argv[1]))
    except (SpecParseError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"{s.title} v{s.version}")
    for e in s.endpoints.values():
        fields = sorted(e.response.fields) if e.response else "-"
        print(f"  {e.key():<24} {e.summary:<20} response fields: {fields}")