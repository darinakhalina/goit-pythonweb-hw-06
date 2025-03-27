from sqlalchemy import func
from connect import session
from models import Student, Grade, Subject


def select_1():
    result = (
        session.query(
            Student.id, Student.name, func.avg(Grade.grade).label("avg_grade")
        )
        .join(Grade, Grade.student_id == Student.id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )

    return result


def select_2(subject_name: str):
    result = (
        session.query(
            Student.id, Student.name, func.avg(Grade.grade).label("avg_grade")
        )
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
        .all()
    )

    return result


def main():
    result1 = select_1()
    print("Top 5 students with the highest average grades:")
    for student in result1:
        print(
            f"Student ID: {student.id}, Name: {student.name}, Average Grade: {student.avg_grade}"
        )

    subject_name = "Mathematics"
    result2 = select_2(subject_name)
    print(f"Student with the highest average grade in {subject_name}:")
    for student in result2:
        print(
            f"Student ID: {student.id}, Name: {student.name}, Average Grade: {student.avg_grade}"
        )


if __name__ == "__main__":
    main()
