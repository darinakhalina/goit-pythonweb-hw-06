from sqlalchemy import func
from connect import session
from models import Student, Grade, Subject, Group, Teacher


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


def select_5(teacher_name: str):
    result = (
        session.query(Subject.name)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    session.close()
    return [subject.name for subject in result]


def select_6(group_name: str):
    result = (
        session.query(Student.name)
        .join(Group, Group.id == Student.group_id)
        .filter(Group.name == group_name)
        .all()
    )
    session.close()
    return [student.name for student in result]


def select_7(group_name: str, subject_name: str):
    result = (
        session.query(Student.name, Grade.grade)
        .join(Group, Group.id == Student.group_id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
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

    teacher_name = "Jessica Freeman"
    result5 = select_5(teacher_name)
    print(f"Courses taught by {teacher_name}:")
    for subject in result5:
        print(f"- {subject}")

    group_name = "Group 1"
    result6 = select_6(group_name)
    print(f"Students in group '{group_name}':")
    for student in result6:
        print(f"- {student}")

    group_name = "Group 1"
    subject_name = "Mathematics"
    result7 = select_7(group_name, subject_name)
    print(f"Grades for students in group '{group_name}' for subject '{subject_name}':")
    for student_name, grade in result7:
        print(f"Student: {student_name}, Grade: {grade}")


if __name__ == "__main__":
    main()
