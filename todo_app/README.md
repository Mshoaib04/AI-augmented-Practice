# Worklist

Worklist is a single-page Flask task manager for keeping team work organized. Add tasks with a name, priority, category, and due date; the task table is sorted by due date, and each task can be deleted from its row.

Tasks are stored in an in-memory Python list. They are not saved to disk or a database, so they are cleared when the application stops.

## Requirements

- Python 3
- Flask

## Set Up

From the project directory, create and activate a virtual environment.

Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Install Flask in the active environment:

```bash
python -m pip install Flask
```

## Run

With the virtual environment active, start the development server from the project directory:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. The app runs with Flask's debug mode enabled, so use it for local development only.