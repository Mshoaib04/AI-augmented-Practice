from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database import Base, get_db
from main import app


def test_department_and_student_workflow(tmp_path) -> None:
    database_path = tmp_path / "test_college.db"
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
            assert client.get("/").json() == {
                "status": "College Management API is running"
            }

            first_department = client.post(
                "/api/departments/",
                json={"department_name": "Computer Science"},
            )
            second_department = client.post(
                "/api/departments/",
                json={"department_name": "Mechanical Engineering"},
            )
            assert first_department.status_code == 201
            assert first_department.json() == {
                "department_id": 1,
                "department_name": "Computer Science",
            }
            assert second_department.status_code == 201

            department_list = client.get("/api/departments/")
            assert department_list.status_code == 200
            assert department_list.json() == [
                {"department_id": 1, "department_name": "Computer Science"},
                {
                    "department_id": 2,
                    "department_name": "Mechanical Engineering",
                },
            ]

            first_student = client.post(
                "/api/students/",
                json={"student_name": "Asha Rao", "department_id": 1},
            )
            second_student = client.post(
                "/api/students/",
                json={"student_name": "Rahul Mehta", "department_id": 2},
            )
            assert first_student.status_code == 201
            assert first_student.json() == {
                "student_id": 1,
                "student_name": "Asha Rao",
                "department_id": 1,
                "department_name": "Computer Science",
            }
            assert second_student.status_code == 201
            assert second_student.json()["department_name"] == "Mechanical Engineering"

            student_list = client.get("/api/students/")
            assert student_list.status_code == 200
            assert [student["department_name"] for student in student_list.json()] == [
                "Computer Science",
                "Mechanical Engineering",
            ]

            missing_department = client.post(
                "/api/students/",
                json={"student_name": "Ram", "department_id": 10},
            )
            assert missing_department.status_code == 404
            assert missing_department.json() == {"detail": "Department not found"}
    finally:
        app.dependency_overrides.clear()
        test_engine.dispose()