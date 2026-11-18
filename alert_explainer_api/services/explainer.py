"""Rule-based plain-language alert explanations."""

from models import Alert

NEXT_STEPS = {
    "critical": "Investigate immediately and take corrective action.",
    "warning": "Review the affected system and monitor the metric closely.",
    "info": "Review the metric and confirm whether any action is needed.",
}


def generate_explanation(alert: Alert) -> str:
    if alert.metric_value > alert.threshold:
        comparison = "exceeded"
    elif alert.metric_value < alert.threshold:
        comparison = "fell below"
    else:
        comparison = "reached"

    acknowledgement = "Not yet acknowledged"

    return (
        f'This {alert.severity} alert from {alert.source} is titled "{alert.title}". '
        f"The {alert.metric_name} metric {comparison} its threshold: the current "
        f"value is {float(alert.metric_value)}, compared with a threshold of "
        f"{float(alert.threshold)}. Recommended next step: "
        f"{NEXT_STEPS[alert.severity]} "
        f"Acknowledged by: {acknowledgement}."
    )