from sqlalchemy import func
from connect import session
from models import Student, Grade, Subject, Group


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

    session.close()
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

    session.close()
    return result


def select_3(subject_name: str):
    result = (
        session.query(Group.id, Group.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
        .all()
    )

    session.close()
    return result


def select_4():
    result = session.query(func.avg(Grade.grade).label("avg_grade")).scalar()

    session.close()
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

    subject_name = "Mathematics"
    result3 = select_3(subject_name)
    print(f"Average grade in groups for the subject '{subject_name}':")
    for group in result3:
        print(
            f"Group ID: {group.id}, Name: {group.name}, Average Grade: {group.avg_grade:.2f}"
        )

    result4 = select_4()
    print(f"Average grade for the entire course: {result4:.2f}")


if __name__ == "__main__":
    main()
