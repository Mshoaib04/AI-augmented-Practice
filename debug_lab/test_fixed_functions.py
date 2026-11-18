from buggy_functions import (
    average_response_time,
    format_alert_summary,
    get_alert_owner,
)


def test_format_alert_summary_with_int_count():
    assert format_alert_summary(3, "critical") == (
        "There are 3 critical alerts active."
    )


def test_get_alert_owner_known_team():
    team_directory = {"db-team": "Asha Patel", "api-team": "Jordan Lee"}
    alert = {"id": 6, "owner": "db-team"}
    assert get_alert_owner(alert, team_directory) == "Asha Patel"


def test_get_alert_owner_unknown_team_returns_fallback():
    team_directory = {"db-team": "Asha Patel", "api-team": "Jordan Lee"}
    alert = {"id": 5, "owner": "network-team"}
    assert get_alert_owner(alert, team_directory) == "Unassigned"


def test_average_response_time_normal_list():
    assert average_response_time([120, 80, 100]) == 100.0


def test_average_response_time_empty_list_returns_zero():
    assert average_response_time([]) == 0.0


def test_format_alert_summary_with_zero_count():
    assert format_alert_summary(0, "info") == "There are 0 info alerts active."


def test_get_alert_owner_with_empty_directory():
    assert get_alert_owner({"owner": "api-team"}, {}) == "Unassigned"


def test_average_response_time_with_single_value():
    assert average_response_time([42.5]) == 42.5


def test_average_response_time_with_zero_values():
    assert average_response_time([0, 0]) == 0.0
