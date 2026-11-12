from pathlib import Path
import pytest
from orchestrator.models import SpecParseError
from orchestrator.spec_parser import extract_endpoints, load_spec, parse_spec

SAMPLES = Path(__file__).parent.parent / "samples"


def test_parse_json():
    spec = parse_spec(load_spec(SAMPLES / "shop_v1.json"))
    assert spec.title == "Shop API" and spec.version == "1.0"
    assert spec.endpoint_keys() == {"GET /customers", "POST /customers", "GET /customers/{id}"}
    cust = spec.get("GET", "/customers").response
    assert cust.name == "Customer"
    assert cust.fields == {"id": "integer", "email": "string", "name": "string"}
    assert cust.required == ["id", "email"]


def test_parse_yaml_with_int_status_codes():
    spec = parse_spec(load_spec(SAMPLES / "shop_v2.yaml"))
    assert spec.version == "2.0"
    assert spec.endpoint_keys() == {"GET /customers", "POST /customers", "GET /orders"}
    assert spec.get("GET", "/customers").response.fields["id"] == "string"
    assert spec.get("GET", "/orders").response.fields == {"order_id": "string"}


def test_extract_endpoints():
    items = extract_endpoints(load_spec(SAMPLES / "shop_v1.json"))
    assert {"path": "/customers", "method": "GET", "summary": "List customers"} in items


def test_errors(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    with pytest.raises(SpecParseError):
        load_spec(bad)
    nopaths = tmp_path / "x.json"
    nopaths.write_text('{"info": {}}')
    with pytest.raises(SpecParseError):
        parse_spec(load_spec(nopaths))
    txt = tmp_path / "x.txt"
    txt.write_text("a")
    with pytest.raises(SpecParseError):
        load_spec(txt)
    with pytest.raises(FileNotFoundError):
        load_spec(tmp_path / "missing.json")