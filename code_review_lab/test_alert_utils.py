import sqlite3

import pytest

from alert_utils import format_alert_message, get_alerts_by_source


def test_critical_message_matches_before_behavior() -> None:
    message = format_alert_message(
        "CRITICAL",
        "CPU spike",
        "api-gateway",
        "cpu_utilization",
        96.5,
        85.0,
    )

    assert message == (
        "CRITICAL ALERT: CPU spike from api-gateway. "
        "cpu_utilization reached 96.5, threshold is 85.0."
    )


def test_unknown_level_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Unknown alert level"):
        format_alert_message("EMERGENCY", "x", "y", "z", 1, 1)


def test_sql_injection_payload_is_treated_as_literal_value(tmp_path) -> None:
    database_path = tmp_path / "alerts.db"
    with sqlite3.connect(database_path) as connection:
        connection.execute("CREATE TABLE alerts (id INTEGER PRIMARY KEY, source TEXT)")
        connection.executemany(
            "INSERT INTO alerts (source) VALUES (?)",
            [("api-gateway",), ("network-monitor",)],
        )

    assert len(get_alerts_by_source(str(database_path), "api-gateway")) == 1
    assert get_alerts_by_source(
        str(database_path),
        "nonexistent' OR '1'='1",
    ) == []


def test_empty_source_name_is_rejected() -> None:
    with pytest.raises(ValueError, match="non-empty string"):
        get_alerts_by_source("unused.db", "")