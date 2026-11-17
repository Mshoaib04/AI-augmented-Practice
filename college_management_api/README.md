# College Management API

FastAPI service backed by SQLAlchemy 2.0 and a project-local SQLite database.

## Set up

From this directory, create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`; interactive documentation is at `http://127.0.0.1:8000/docs`.

## Routes

- `GET /api/departments/`
- `POST /api/departments/`
- `GET /api/students/`
- `POST /api/students/`

## Test

```bash
python -m pytest
```