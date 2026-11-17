"""Create and seed the college API database."""

from connection import getSqliteConnection


DEPARTMENTS = [
    (1, "Computer Science"),
    (2, "Electrical Engineering"),
    (3, "Mechanical Engineering"),
    (4, "Mathematics"),
    (5, "Physics"),
]

STUDENTS = [
    (101, "Alice Johnson", 1),
    (102, "Bob Smith", 2),
    (103, "Carol Lee", 3),
    (104, "David Brown", 4),
    (105, "Emily White", 5),
]


def initialize_database():
    """Recreate and seed the departments and students tables."""
    connection = getSqliteConnection()
    try:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS students")
        cursor.execute("DROP TABLE IF EXISTS departments")
        cursor.execute(
            """
            CREATE TABLE departments (
                DepartmentId INTEGER PRIMARY KEY,
                DepartmentName TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE students (
                StudentId INTEGER PRIMARY KEY,
                StudentName TEXT NOT NULL,
                DepartmentId INTEGER,
                FOREIGN KEY (DepartmentId) REFERENCES departments (DepartmentId)
            )
            """
        )
        cursor.executemany(
            "INSERT INTO departments (DepartmentId, DepartmentName) VALUES (?, ?)",
            DEPARTMENTS,
        )
        cursor.executemany(
            "INSERT INTO students (StudentId, StudentName, DepartmentId) VALUES (?, ?, ?)",
            STUDENTS,
        )
        connection.commit()
        department_count = cursor.execute(
            "SELECT COUNT(*) FROM departments"
        ).fetchone()[0]
        student_count = cursor.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        return department_count, student_count
    finally:
        connection.close()


if __name__ == "__main__":
    departments_inserted, students_inserted = initialize_database()
    print(
        f"{departments_inserted} departments and "
        f"{students_inserted} students inserted."
    )