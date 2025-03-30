import logging
from sqlalchemy import func
from connect import session
from models import Student, Grade, Subject, Group, Teacher

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


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


def select_8(teacher_name: str):
    result = (
        session.query(func.avg(Grade.grade).label("avg_grade"))
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    session.close()
    return result


def select_9(student_id: str):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )
    session.close()
    return result


def select_10(student_id: str, teacher_id: str):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )
    session.close()
    return result


def select_11(student_id: str, teacher_id: str):
    result = (
        session.query(func.avg(Grade.grade))
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .scalar()
    )
    session.close()
    return result


def select_12(group_name: str, subject_name: str):
    subquery = (
        session.query(func.max(Grade.date))
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .scalar_subquery()
    )

    result = (
        session.query(Student.name, Grade.grade, Grade.date)
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(
            Group.name == group_name,
            Subject.name == subject_name,
            Grade.date == subquery,
        )
        .all()
    )

    session.close()
    return result


def main():
    result1 = select_1()
    logger.info("Top 5 students with the highest average grades:")
    for student in result1:
        logger.info(
            f"Student ID: {student.id}, Name: {student.name}, Average Grade: {student.avg_grade}"
        )

    subject_name = "Mathematics"
    result2 = select_2(subject_name)
    logger.info(f"Student with the highest average grade in {subject_name}:")
    for student in result2:
        logger.info(
            f"Student ID: {student.id}, Name: {student.name}, Average Grade: {student.avg_grade}"
        )

    subject_name = "Mathematics"
    result3 = select_3(subject_name)
    logger.info(f"Average grade in groups for the subject '{subject_name}':")
    for group in result3:
        logger.info(
            f"Group ID: {group.id}, Name: {group.name}, Average Grade: {group.avg_grade:.2f}"
        )

    result4 = select_4()
    logger.info(f"Average grade for the entire course: {result4:.2f}")

    teacher_name = "Jessica Freeman"
    result5 = select_5(teacher_name)
    logger.info(f"Courses taught by {teacher_name}:")
    for subject in result5:
        logger.info(f"- {subject}")

    group_name = "Group 1"
    result6 = select_6(group_name)
    logger.info(f"Students in group '{group_name}':")
    for student in result6:
        logger.info(f"- {student}")

    group_name = "Group 1"
    subject_name = "Mathematics"
    result7 = select_7(group_name, subject_name)
    logger.info(
        f"Grades for students in group '{group_name}' for subject '{subject_name}':"
    )
    for student_name, grade in result7:
        logger.info(f"Student: {student_name}, Grade: {grade}")

    teacher_name = "Kayla Jones"
    result8 = select_8(teacher_name)
    logger.info(f"Average grade given by {teacher_name}: {result8}")

    student_id = "1"
    result9 = select_9(student_id)
    for course in result9:
        logger.info(course[0])

    student_id = "1"
    teacher_id = "1"
    subjects = select_10(student_id, teacher_id)
    logger.info(f"Courses taught by {teacher_name} for {student_name}:")
    for subject in subjects:
        logger.info(subject.name)

    student_id = "1"
    teacher_id = "1"
    result11 = select_11(student_id, teacher_id)
    logger.info(
        f"The average grade given by teacher {teacher_id} to student {student_id}: {result11}"
    )

    group_name = "Group 1"
    subject_name = "Mathematics"
    result12 = select_12(group_name, subject_name)
    logger.info(f"Latest grades in group '{group_name}' for subject '{subject_name}':")
    for student_name, grade, date in result12:
        logger.info(f"Student: {student_name}, Grade: {grade}, Date: {date}")


if __name__ == "__main__":
    main()
