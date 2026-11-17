# College API

A small Flask API backed by a seeded SQLite database.

## Set up

From this directory, install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Initialize and run

Create or reset `studentDB.db` with the five departments and five students:

```bash
python init_db.py
```

Start the API:

```bash
python boilerCode.py
```

The API is available at `http://127.0.0.1:5000`. It provides `GET /studentDepartments` and `GET /departments`.

## Test

```bash
python -m pytest
```