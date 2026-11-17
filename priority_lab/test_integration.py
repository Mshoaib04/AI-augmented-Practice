from collections.abc import Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import main
from models import Alert
from priority_score import calculate_priority_score


@pytest.fixture
def test_context(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[tuple[TestClient, sessionmaker[Session]], None, None]:
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )
    monkeypatch.setattr(main, "engine", test_engine)
    main.Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[main.get_db] = override_get_db
    try:
        with TestClient(main.app) as client:
            yield client, session_factory
    finally:
        main.app.dependency_overrides.pop(main.get_db, None)
        test_engine.dispose()


def test_priority_endpoint_returns_score(test_context) -> None:
    client, session_factory = test_context
    with session_factory() as db:
        alert = Alert(severity="critical", metric_value=125, threshold=100)
        db.add(alert)
        db.commit()
        db.refresh(alert)
        alert_id = alert.id

    response = client.get(f"/alerts/{alert_id}/priority")

    assert response.status_code == 200
    assert response.json() == {
        "alert_id": alert_id,
        "priority_score": calculate_priority_score("critical", 125, 100),
    }


def test_nonexistent_alert_returns_404(test_context) -> None:
    client, _session_factory = test_context

    response = client.get("/alerts/999/priority")

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"


def test_zero_threshold_alert_returns_422(test_context) -> None:
    client, session_factory = test_context
    with session_factory() as db:
        alert = Alert(severity="warning", metric_value=50, threshold=0)
        db.add(alert)
        db.commit()
        db.refresh(alert)
        alert_id = alert.id

    response = client.get(f"/alerts/{alert_id}/priority")

    assert response.status_code == 422
    assert "threshold must not be zero" in response.json()["detail"]