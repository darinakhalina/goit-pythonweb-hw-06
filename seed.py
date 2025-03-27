from faker import Faker
from models import Student, Group, Teacher, Subject, Grade
from connect import session

faker = Faker()


def main():
    groups = [Group(name=f"Group {i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()
    group_ids = [group.id for group in groups]

    teachers = [Teacher(name=faker.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()
    teacher_ids = [teacher.id for teacher in teachers]

    subjects = [
        Subject(
            name=f"Subject {faker.word()}",
            teacher_id=faker.random.choice(teacher_ids),
        )
        for _ in range(1, 9)
    ]
    session.add_all(subjects)
    session.commit()
    subject_ids = [subject.id for subject in subjects]

    students = [
        Student(
            name=faker.name(),
            group_id=faker.random.choice(group_ids),
        )
        for _ in range(50)
    ]
    session.add_all(students)
    session.commit()
    student_ids = [student.id for student in students]

    # Создаем оценки
    grades = [
        Grade(
            student_id=faker.random.choice(student_ids),
            subject_id=faker.random.choice(subject_ids),
            grade=faker.random.randint(1, 5),
            date=faker.date_this_year(),
        )
        for _ in range(20 * len(students))
    ]
    session.add_all(grades)
    session.commit()


if __name__ == "__main__":
    main()
