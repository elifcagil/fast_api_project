from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic



Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    category_name = Column(String, index=True)
    category_type = Column(String, index=True)


class CategoryPydantic(BaseModel): #sqlalchemy modeline göre pydantic modelini olusturdu.gelen ve giden verileri doğrulama ve dönüştürmek için kullandık
    category_id: int
    category_name: str
    category_type: str

CategoryPydantic = sqlalchemy_to_pydantic(Category, exclude=['category_id'])
