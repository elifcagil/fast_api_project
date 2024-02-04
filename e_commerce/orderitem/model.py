from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OrderItem(Base):
    __tablename__ = "orderitem"

    detail_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id', ondelete='CASCADE'), index=True)
    product_id = Column(Integer, ForeignKey('product.product_id', ondelete='CASCADE'), index=True)
    quantity = Column(Integer)
    subtotal = Column(Float, index=True)



class OrderItemPydantic(BaseModel):
    detail_id: int
    order_id: int
    product_id: int
    quantity: int
    subtotal: float

OrderItemPydantic = sqlalchemy_to_pydantic(OrderItem, exclude=['detail_id']) #SQLAlchemy modelini Pydantic modeline dönüştür
