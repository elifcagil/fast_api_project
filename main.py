from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from e_commerce.product.router import router as product_router
from e_commerce.categories.router import router as categories_router
from e_commerce.orderitem.router import router as orderitem_router
from e_commerce.orders.router import router as orders_router
from e_commerce.user.router import router as user_router

from e_commerce.database import Base, engine

Base.metadata.create_all(bind=engine)

class Config:
    arbitrary_types_allowed = True


DATABASE_URL = "postgresql://postgres:123456@localhost/newproject"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)  # Tabloları oluştur

app = FastAPI()
app.include_router(categories_router, prefix="/api")
app.include_router(product_router, prefix="/api")
app.include_router(orderitem_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(user_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
