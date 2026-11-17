from collections.abc import Generator
from datetime import datetime

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from models import Alert


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    test_session_local = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )
    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = test_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        test_engine.dispose()


def _create_alert(client: TestClient, **overrides: str | float) -> dict:
    payload: dict[str, str | float] = {
        "title": "Test alert",
        "severity": "warning",
        "source": "test-source",
        "metric_name": "test_metric",
        "metric_value": 50.0,
        "threshold": 40.0,
    }
    payload.update(overrides)
    response = client.post("/alerts/", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_alert(client: TestClient) -> None:
    response = client.post(
        "/alerts/",
        json={
            "title": "High CPU",
            "severity": "critical",
            "source": "api-gateway",
            "metric_name": "cpu_utilization",
            "metric_value": 96.5,
            "threshold": 85.0,
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["severity"] == "critical"


def test_list_alerts(client: TestClient) -> None:
    _create_alert(client, title="First alert")
    _create_alert(client, title="Second alert")

    response = client.get("/alerts/")

    assert response.status_code == 200
    assert [alert["title"] for alert in response.json()] == [
        "First alert",
        "Second alert",
    ]


def test_get_alert_by_id(client: TestClient) -> None:
    alert = _create_alert(client)

    response = client.get(f"/alerts/{alert['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == alert["id"]
    assert response.json()["metric_name"] == "test_metric"


def test_explain_alert(client: TestClient) -> None:
    alert = _create_alert(client, severity="critical")

    response = client.post(f"/alerts/{alert['id']}/explain")

    assert response.status_code == 200
    body = response.json()
    assert body["alert_id"] == alert["id"]
    assert "critical" in body["explanation"]
    assert "test_metric" in body["explanation"]
    datetime.fromisoformat(body["generated_at"].replace("Z", "+00:00"))


def test_explain_alert_for_nonexistent_id_returns_404(client: TestClient) -> None:
    response = client.post("/alerts/999/explain")

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"


def test_explain_alert_when_metric_is_below_threshold(client: TestClient) -> None:
    alert = _create_alert(client, metric_value=2, threshold=10)

    response = client.post(f"/alerts/{alert['id']}/explain")

    assert response.status_code == 200
    assert "fell below its threshold" in response.json()["explanation"]


def test_explain_alert_with_zero_threshold_does_not_crash(
    client: TestClient,
) -> None:
    alert = _create_alert(client, metric_value=5, threshold=0)

    response = client.post(f"/alerts/{alert['id']}/explain")

    assert response.status_code == 200
    assert "threshold of 0.0" in response.json()["explanation"]