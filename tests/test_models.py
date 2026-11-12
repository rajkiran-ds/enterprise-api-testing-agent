import pytest
from orchestrator.models import APISpec, DuplicateEndpointError, Endpoint, Schema


def test_schema_fields_and_fresh_required():
    cust = Schema("Customer", {"id": "integer", "email": "string"}, ["id"])
    other = Schema("Other", {"x": "string"})
    assert cust.field_names() == {"id", "email"}
    assert other.required == [] and other.required is not cust.required


def test_apispec_endpoints():
    spec = APISpec("Shop", "1.0")
    spec.add_endpoint(Endpoint("get", "/customers", "list"))
    spec.add_endpoint(Endpoint("POST", "/customers"))
    assert spec.endpoint_keys() == {"GET /customers", "POST /customers"}
    assert spec.get("GET", "/customers").summary == "list"
    assert spec.get("DELETE", "/x") is None


def test_duplicate_endpoint():
    spec = APISpec("Shop", "1.0")
    spec.add_endpoint(Endpoint("GET", "/a"))
    with pytest.raises(DuplicateEndpointError):
        spec.add_endpoint(Endpoint("get", "/a"))


def test_specs_do_not_share_endpoints():
    a, b = APISpec("A", "1"), APISpec("B", "1")
    a.add_endpoint(Endpoint("GET", "/x"))
    assert b.endpoint_keys() == set()