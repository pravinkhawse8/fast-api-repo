from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



db_url ="postgresql://postgres:postgres@localhost:5432/hruta_db"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)