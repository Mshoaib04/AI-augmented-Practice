"""SQLite connection helper for the college API."""

import sqlite3
from pathlib import Path


def getSqliteConnection():
    """Return a connection to the project-local student database."""
    connection = sqlite3.connect(Path(__file__).with_name("studentDB.db"))
    connection.execute("PRAGMA foreign_keys = ON")
    return connection