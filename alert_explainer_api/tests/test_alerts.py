from collections.abc import Generator
from datetime import datetime

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database import Base, get_db
from main import app
from models import Alert
from services.explainer import generate_explanation


@pytest.mark.parametrize(
    ("metric_value", "comparison"),
    [(96.5, "exceeded"), (80.0, "fell below"), (85.0, "reached")],
)
def test_explanation_describes_metric_comparison(
    metric_value: float,
    comparison: str,
) -> None:
    alert = Alert(
        title="Threshold check",
        severity="info",
        source="test-monitor",
        metric_name="test_metric",
        metric_value=metric_value,
        threshold=85.0,
    )

    assert f"metric {comparison} its threshold" in generate_explanation(alert)


def test_alert_explainer_workflow(tmp_path) -> None:
    database_path = tmp_path / "test_alerts.db"
    test_engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )
    TestSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )
    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as client:
            assert client.get("/").status_code == 200

            critical_alert = client.post(
                "/alerts/",
                json={
                    "title": "High CPU utilization on api-gateway-prod-3",
                    "severity": "critical",
                    "source": "api-gateway",
                    "metric_name": "cpu_utilization",
                    "metric_value": 96.5,
                    "threshold": 85.0,
                },
            )
            warning_alert = client.post(
                "/alerts/",
                json={
                    "title": "Elevated response latency on network-monitor",
                    "severity": "warning",
                    "source": "network-monitor",
                    "metric_name": "p95_latency_ms",
                    "metric_value": 812,
                    "threshold": 500,
                },
            )

            assert critical_alert.status_code == 201
            assert critical_alert.json()["id"] == 1
            created_at = datetime.fromisoformat(
                critical_alert.json()["created_at"].replace("Z", "+00:00")
            )
            assert created_at.utcoffset() is not None
            assert created_at.utcoffset().total_seconds() == 0
            assert warning_alert.status_code == 201
            assert warning_alert.json()["id"] == 2

            alert_list = client.get("/alerts/")
            assert alert_list.status_code == 200
            assert [alert["id"] for alert in alert_list.json()] == [1, 2]
            assert client.get("/alerts/1").json() == critical_alert.json()

            critical_explanation = client.post("/alerts/1/explain")
            assert critical_explanation.status_code == 200
            assert critical_explanation.json()["alert_id"] == 1
            assert critical_explanation.json()["explanation"] == (
                'This critical alert from api-gateway is titled "High CPU utilization '
                'on api-gateway-prod-3". The cpu_utilization metric exceeded its '
                "threshold: the current value is 96.5, compared with a threshold of "
                "85.0. Recommended next step: Investigate immediately and take "
                "corrective action."
            )
            datetime.fromisoformat(
                critical_explanation.json()["generated_at"].replace("Z", "+00:00")
            )

            warning_explanation = client.post("/alerts/2/explain")
            assert warning_explanation.status_code == 200
            assert warning_explanation.json()["explanation"] == (
                'This warning alert from network-monitor is titled "Elevated response '
                'latency on network-monitor". The p95_latency_ms metric exceeded its '
                "threshold: the current value is 812.0, compared with a threshold of "
                "500.0. Recommended next step: Review the affected system and monitor "
                "the metric closely."
            )

            unknown_alert = client.get("/alerts/999")
            assert unknown_alert.status_code == 404
            assert unknown_alert.json() == {"detail": "Alert not found"}
            unknown_explanation = client.post("/alerts/999/explain")
            assert unknown_explanation.status_code == 404
            assert unknown_explanation.json() == {"detail": "Alert not found"}

            invalid_severity = client.post(
                "/alerts/",
                json={
                    "title": "Invalid severity",
                    "severity": "urgent",
                    "source": "test",
                    "metric_name": "test_metric",
                    "metric_value": 1,
                    "threshold": 0,
                },
            )
            assert invalid_severity.status_code == 422
    finally:
        app.dependency_overrides.clear()
        test_engine.dispose()