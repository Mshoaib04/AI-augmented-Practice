# Alert Explainer API

A FastAPI service that stores monitoring alerts in SQLite and generates deterministic, rule-based explanations. It does not call an external AI service.

## Set up

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`; Swagger UI is at `http://127.0.0.1:8000/docs`.

## Routes

- `POST /alerts/` creates an alert.
- `GET /alerts/` lists alerts.
- `GET /alerts/{alert_id}` retrieves one alert.
- `POST /alerts/{alert_id}/explain` returns a plain-language explanation.

Explanations include `Acknowledged by: Not yet acknowledged.` The current
`Alert` model has no `resolved_by` field; this is a fixed acknowledgement
message, not a persisted acknowledgement or a new model field.

## Test

```bash
python -m pytest
```

The troubleshooting lab adds an unresolved-acknowledgement regression test
to the seven original API tests in `tests/test_alerts.py`.