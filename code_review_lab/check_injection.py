"""Demonstrate that an SQL injection payload is treated as a literal value."""

import sqlite3
from tempfile import TemporaryDirectory
from pathlib import Path

from alert_utils import get_alerts_by_source


with TemporaryDirectory() as directory:
    database_path = Path(directory) / "alerts_demo.db"
    with sqlite3.connect(database_path) as connection:
        connection.execute("CREATE TABLE alerts (id INTEGER PRIMARY KEY, source TEXT)")
        connection.executemany(
            "INSERT INTO alerts (source) VALUES (?)",
            [("api-gateway",), ("network-monitor",)],
        )

    print("Normal lookup:   ", get_alerts_by_source(str(database_path), "api-gateway"))
    print(
        "Injection lookup:",
        get_alerts_by_source(str(database_path), "nonexistent' OR '1'='1"),
    )