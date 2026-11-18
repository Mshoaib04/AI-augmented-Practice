def format_alert_summary(alert_count, severity):
    return f"There are {alert_count} {severity} alerts active."


def get_alert_owner(alert, team_directory):
    return team_directory.get(alert["owner"], "Unassigned")


def average_response_time(response_times):
    if not response_times:
        return 0.0
    return sum(response_times) / len(response_times)


if __name__ == "__main__":
    print(format_alert_summary(3, "critical"))
    alert = {"id": 5, "owner": "network-team"}
    team_directory = {
        "db-team": "Asha Patel",
        "api-team": "Jordan Lee",
    }
    print(get_alert_owner(alert, team_directory))
    print(average_response_time([]))
