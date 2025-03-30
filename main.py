import argparse
import logging
from datetime import datetime
from connect import session
from models import Student, Group, Teacher, Subject, Grade

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

MODELS = {
    "Student": Student,
    "Group": Group,
    "Teacher": Teacher,
    "Subject": Subject,
    "Grade": Grade,
}


def create(model_name: str, **kwargs):
    model = MODELS.get(model_name)
    if not model:
        logger.error(f"Unknown model '{model_name}'")
        return

    kwargs.pop("action", None)

    model_fields = {field.name for field in model.__table__.columns}

    kwargs = {k: v for k, v in kwargs.items() if k in model_fields}

    required_fields = {
        "Student": ["name", "group_id"],
        "Teacher": ["name"],
        "Group": ["name"],
        "Subject": ["name", "teacher_id"],
        "Grade": ["student_id", "subject_id", "grade", "date"],
    }

    missing_fields = required_fields.get(model_name, [])
    for field in missing_fields:
        if field not in kwargs:
            logger.error(f"Missing required field '{field}' for {model_name}")
            return

    if model_name == "Grade":
        kwargs["date"] = datetime.strptime(kwargs["date"], "%Y-%m-%d")

    try:
        entity = model(**kwargs)
        session.add(entity)
        session.commit()
        logger.info(f"{model_name} added with ID {entity.id}")

    except Exception as e:
        session.rollback()
        logger.error(f"Error creating {model_name}: {e}")


def list_entities(model_name: str):
    model = MODELS.get(model_name)
    if not model:
        logger.error(f"Unknown model '{model_name}'")
        return

    entities = session.query(model).all()
    if entities:
        for entity in entities:
            logger.info(entity.__dict__)
    else:
        logger.error(f"No {model_name.lower()}s found.")


def update(model_name: str, entity_id: int, **kwargs):
    model = MODELS.get(model_name)
    if not model:
        logger.error(f"Unknown model '{model_name}'")
        return

    entity = session.query(model).filter_by(id=entity_id).first()
    if entity:
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        session.commit()
        logger.info(f"{model_name} ID {entity_id} updated")
    else:
        logger.error(f"{model_name} not found")


def remove(model_name: str, entity_id: int):
    model = MODELS.get(model_name)
    if not model:
        logger.error(f"Unknown model '{model_name}'")
        return

    entity = session.query(model).filter_by(id=entity_id).first()
    if entity:
        session.delete(entity)
        session.commit()
        logger.info(f"{model_name} ID {entity_id} removed")
    else:
        logger.error(f"{model_name} not found")


def main():
    parser = argparse.ArgumentParser(description="CLI for database management")
    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "list", "update", "remove"],
        required=True,
        help="CRUD action",
    )
    parser.add_argument(
        "-m", "--model", choices=MODELS.keys(), required=True, help="Database model"
    )
    parser.add_argument("--id", type=int, help="ID of the entity (for update/remove)")
    parser.add_argument(
        "--name", type=str, help="Name of the entity (for create/update)"
    )
    parser.add_argument("--group_id", type=int, help="Group ID (for Student)")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID (for Subject)")
    parser.add_argument("--student_id", type=int, help="Student ID (for Grade)")
    parser.add_argument("--subject_id", type=int, help="Subject ID (for Grade)")
    parser.add_argument("--grade", type=int, help="Grade (for Grade)")
    parser.add_argument("--date", type=str, help="Date (YYYY-MM-DD) for Grade")

    args = parser.parse_args()

    kwargs = {k: v for k, v in vars(args).items() if v is not None}

    kwargs.pop("action", None)

    if args.action == "create":
        create(args.model, **kwargs)
    elif args.action == "list":
        list_entities(args.model)
    elif args.action == "update" and args.id:
        update(args.model, args.id, **kwargs)
    elif args.action == "remove" and args.id:
        remove(args.model, args.id)
    else:
        logger.error("Missing required parameters")


if __name__ == "__main__":
    main()
