import sqlite3

import boilerCode
import init_db


def test_database_seed_and_api_endpoints(tmp_path, monkeypatch):
    database_path = tmp_path / "studentDB.db"
    connect_to_test_database = lambda: sqlite3.connect(database_path)
    monkeypatch.setattr(init_db, "getSqliteConnection", connect_to_test_database)
    monkeypatch.setattr(boilerCode, "getSqliteConnection", connect_to_test_database)

    assert init_db.initialize_database() == (5, 5)

    client = boilerCode.app.test_client()
    index_response = client.get("/")
    students_response = client.get("/studentDepartments")
    departments_response = client.get("/departments")

    assert index_response.status_code == 200
    assert index_response.get_json() == {
        "message": "College API is running.",
        "endpoints": {
            "studentDepartments": "/studentDepartments",
            "departments": "/departments",
        },
    }
    assert students_response.status_code == 200
    assert students_response.get_json() == [
        {"StudentName": "Alice Johnson", "DepartmentName": "Computer Science"},
        {"StudentName": "Bob Smith", "DepartmentName": "Electrical Engineering"},
        {"StudentName": "Carol Lee", "DepartmentName": "Mechanical Engineering"},
        {"StudentName": "David Brown", "DepartmentName": "Mathematics"},
        {"StudentName": "Emily White", "DepartmentName": "Physics"},
    ]
    assert departments_response.status_code == 200
    assert departments_response.get_json() == [
        {"DepartmentId": 1, "DepartmentName": "Computer Science"},
        {"DepartmentId": 2, "DepartmentName": "Electrical Engineering"},
        {"DepartmentId": 3, "DepartmentName": "Mechanical Engineering"},
        {"DepartmentId": 4, "DepartmentName": "Mathematics"},
        {"DepartmentId": 5, "DepartmentName": "Physics"},
    ]