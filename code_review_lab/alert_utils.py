"""Alert formatting and safe source-based lookup helpers."""

from contextlib import closing
import os
import sqlite3

ON_CALL_THRESHOLD_MULTIPLIER = 1.5
DB_PASSWORD = os.environ.get("DB_PASSWORD")
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")


def format_alert_message(
    level: str,
    title: str,
    source: str,
    metric_name: str,
    metric_value: float,
    threshold: float,
) -> str:
    """Format a critical or warning alert consistently."""
    if level not in {"CRITICAL", "WARNING"}:
        raise ValueError(f"Unknown alert level: {level}")

    message = f"{level} ALERT: {title} from {source}. "
    message += f"{metric_name} reached {metric_value}, threshold is {threshold}."
    if metric_value > threshold * ON_CALL_THRESHOLD_MULTIPLIER:
        message += " This is over 150% of threshold -- page on-call immediately."
    return message


def get_alerts_by_source(db_path: str, source_name: str) -> list[tuple]:
    """Return alerts for an exact source value using a parameterized query."""
    if not isinstance(source_name, str) or not source_name.strip():
        raise ValueError("source_name must be a non-empty string")

    with closing(sqlite3.connect(db_path)) as conn:
        return conn.execute(
            "SELECT * FROM alerts WHERE source = ?",
            (source_name,),
        ).fetchall()