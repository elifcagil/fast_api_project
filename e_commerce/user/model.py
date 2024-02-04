from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True)
    address = Column(String, index=True)
    email = Column(String, index=True)


class UserPydantic(BaseModel):
    user_id: int
    username: str
    address: str
    email: str



CustomerPydantic = sqlalchemy_to_pydantic(User, exclude=['user_id'])
