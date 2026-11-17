"""Student API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Department, Student
from schemas import StudentCreate, StudentOut

router = APIRouter(prefix="/api/students", tags=["students"])


@router.get("/", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)) -> list[Student]:
    statement = (
        select(Student)
        .options(joinedload(Student.department))
        .order_by(Student.student_id)
    )
    return list(db.scalars(statement).all())


@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(
    student_in: StudentCreate,
    db: Session = Depends(get_db),
) -> Student:
    department = db.get(Department, student_in.department_id)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    student = Student(
        student_name=student_in.student_name,
        department=department,
    )
    db.add(student)
    db.commit()

    statement = (
        select(Student)
        .options(joinedload(Student.department))
        .where(Student.student_id == student.student_id)
    )
    return db.scalar(statement)