"""Data classes describing an API spec. An APISpec HAS Endpoints; an Endpoint HAS a Schema."""


class SpecError(Exception):
    """Base error for API spec problems."""


class DuplicateEndpointError(SpecError):
    """Same method + path added twice."""


class SpecParseError(SpecError):
    """Spec file could not be read or is not valid."""


class Schema:
    def __init__(self, name: str, fields: dict[str, str], required: list[str] | None = None) -> None:
        self.name = name
        self.fields = dict(fields)
        self.required = list(required) if required else []  # fresh list per object

    def field_names(self) -> set[str]:
        return set(self.fields)

    def __repr__(self) -> str:
        return f"Schema({self.name}, {len(self.fields)} fields)"


class Endpoint:
    def __init__(self, method: str, path: str, summary: str = "", response: Schema | None = None) -> None:
        self.method = method.upper()
        self.path = path
        self.summary = summary
        self.response = response

    def key(self) -> str:
        return f"{self.method} {self.path}"

    def __repr__(self) -> str:
        return f"Endpoint({self.key()})"


class APISpec:
    def __init__(self, title: str, version: str) -> None:
        self.title = title
        self.version = version
        self.endpoints: dict[str, Endpoint] = {}

    def add_endpoint(self, endpoint: Endpoint) -> None:
        if endpoint.key() in self.endpoints:
            raise DuplicateEndpointError(f"Duplicate endpoint: {endpoint.key()}")
        self.endpoints[endpoint.key()] = endpoint

    def get(self, method: str, path: str) -> Endpoint | None:
        return self.endpoints.get(f"{method.upper()} {path}")

    def endpoint_keys(self) -> set[str]:
        return set(self.endpoints)