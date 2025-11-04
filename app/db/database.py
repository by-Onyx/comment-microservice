from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

USER = os.getenv('POSTGRES_USER')
PWD = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')

DATABASE_URL = f'postgresql://{USER}:{PWD}@postgres:5432/{DB}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
