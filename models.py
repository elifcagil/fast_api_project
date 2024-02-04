from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from e_commerce.database import SessionLocal
from pydantic import BaseModel
Base = declarative_base()


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()