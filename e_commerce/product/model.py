
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field





Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String(100), nullable=False, index=True)
    description = Column(String, index=True)
    price = Column(Float, nullable=False, index=True)
    stock_quantity = Column(Integer, nullable=False, index=True)


    category_id = Column(Integer, ForeignKey('categories.category_id', ondelete='CASCADE'))




class ProductPydantic(BaseModel):

    product_id: int
    product_name: str
    category_id: int = None
    price: float
    stock_quantity: int
    description: str

    class Config:
        arbitrary_types_allowed = True

class ProductCreate(BaseModel):
    product_name: str
    price: float
    stock_quantity: int
    description: str




ProductPydantic = sqlalchemy_to_pydantic(Product, exclude=['product_id'])



