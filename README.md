# mcp-delegation-lab

A small MCP proof-of-concept that demonstrates delegation-scoped transfer tooling for a mock UNITS-like environment.

This is intentionally minimal: it focuses on scope validation, pre-flight checks, structured tool responses, and audit logs.

## What it includes

- `get_delegation_scope`
- `check_transfer_eligibility`
- `initiate_transfer`
- structured results with error codes
- mock data store and policy engine
- tests and example requests

## Quickstart

Option A (uv):

```bash
uv venv
source .venv/bin/activate
uv sync --extra dev
```

Option B (pip):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run the MCP server (stdio):

```bash
python -m mcp_delegation_lab.server
```

Run tests:

```bash
pytest
```

## Demo (quick)

1. Start the server:

```bash
python -m mcp_delegation_lab.server
```

2. In MCP Inspector, call the tools using the example payloads:

- `get_delegation_scope` -> `examples/get_delegation_scope.json`
- `check_transfer_eligibility` -> `examples/check_transfer_eligibility.json`
- `initiate_transfer` -> `examples/initiate_transfer.json`

## Design notes

- Scope validation runs before any transfer commit.
- `initiate_transfer` always executes a pre-flight policy check.
- Policy failures return `ok: true` with `eligible: false` to avoid tool-level errors.
- No credentials are stored or returned; all data is mocked in memory.

## Schema snapshots

- `examples/get_delegation_scope_schema.json`
- `examples/check_transfer_eligibility_schema.json`
- `examples/initiate_transfer_schema.json`

## What is mocked

- Account balances and delegation records (in-memory store).
- Policy evaluation rules (simple checks).
- Transfer commit (local balance update).

## Tool response example

`check_transfer_eligibility` returns an eligibility object even when ineligible.

```json
{
  "ok": true,
  "audit_id": "b3f8d96b-0bcf-4c2d-bd7f-03f8f3cf6ab0",
  "data": {
    "eligible": false,
    "code": "SCOPE_EXCEEDED",
    "message": "Requested amount exceeds delegated limit.",
    "detail": {
      "token_class": "INR_STABLE",
      "requested_amount": "1500",
      "delegated_limit": "1000",
      "checks_failed": ["amount_limit"],
      "checks_passed": [
        "delegation_active",
        "token_class",
        "from_account_scope",
        "sufficient_balance"
      ]
    }
  }
}
```

## Notes

- This uses the MCP Python SDK. If your SDK entrypoint differs, update `server.py`.
- All data is in-memory. There are no real credentials or network calls.

## Changelog

See `CHANGELOG.md`.

## Repo layout

```
src/mcp_delegation_lab/
  server.py
  tools.py
  handlers.py
  policy.py
  store.py
  models.py
  errors.py
  audit.py
tests/
examples/
```
