from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from e_commerce.database import SessionLocal
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic


Base = declarative_base()


class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    orders_date = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('customer.user_id'), index=True)
    quantity = Column(Integer, index=True)
    total_amount = Column(Float, index=True)


class OrdersPydantic(BaseModel):

    order_id: int
    orders_date: str
    user_id: int
    quantity: int
    total_amount: float


OrdersPydantic = sqlalchemy_to_pydantic(Orders, exclude=['order_id'])
