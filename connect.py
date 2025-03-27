from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

url_to_db = "postgresql://postgres:1239@localhost:5432/db-hw-6"
engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()
