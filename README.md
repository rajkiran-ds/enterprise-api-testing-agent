# Enterprise API Integration & Testing Agent

AI-assisted API compatibility and testing: parse OpenAPI specs, compare schemas deterministically,
use an LLM for mapping suggestions and explanations, generate and run tests with human approval.

Two independent services: **Mock Enterprise API** (`mock_api/`) and **AI Orchestration & Testing Service** (`orchestrator/`).

## Status
Days 1-4: spec models, OpenAPI JSON/YAML parser, config + logging, API design.
Next: FastAPI services (Day 5), auth and service-to-service calls (Day 6).

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
```

## Run
```bash
python -m orchestrator.spec_parser samples/shop_v1.json
python -m orchestrator.spec_parser samples/shop_v2.yaml
python -m pytest
```

## Layout
- `orchestrator/models.py`: Schema, Endpoint, APISpec, errors
- `orchestrator/spec_parser.py`: OpenAPI JSON/YAML parsing (deterministic)
- `orchestrator/schema_compare.py`: comparison logic (stub, Day 7+)
- `mock_api/endpoints.py`: planned mock endpoints
- `samples/`: v1 (JSON) and v2 (YAML) sample specs, with deliberate differences
- `docs/API_DESIGN.md`: endpoints for both services