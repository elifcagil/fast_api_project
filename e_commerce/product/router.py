from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from e_commerce.product.model import Product
from e_commerce.product.model import ProductPydantic


router = APIRouter()


@router.get("/products/")
def read_products(product_id: int = None, db: Session = Depends(get_db)):
    if product_id:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı")
        return product
    else:
        products = db.query(Product).all()
        return products


@router.put("/products/{product_id}", response_model=ProductPydantic)
def update_product(product_id: int, updated_product: ProductPydantic, db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.product_id == product_id).first()
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    # Güncelleme işlemi
    existing_product.product_name = updated_product.product_name
    existing_product.category_id = updated_product.category_id
    existing_product.price = updated_product.price
    existing_product.stock_quantity = updated_product.stock_quantity
    existing_product.description = updated_product.description

    db.commit()
    db.refresh(existing_product)
    return existing_product


@router.post("/products/", response_model=ProductPydantic)
def create_product(
    product_name: str, category_id: int, price: float, stock_quantity: int, description: str,
    db: Session = Depends(get_db)
):
    new_product = Product(
        product_name=product_name, category_id=category_id, price=price,
        stock_quantity=stock_quantity, description=description
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    db.delete(product)
    db.commit()
    return {"message": "Ürün başarıyla silindi"}


'''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from e_commerce.product.model import Product
from e_commerce.product.model import ProductPydantic


router = APIRouter()


@router.get("/products/")
def read_products(product_id: int = None, db: Session = Depends(get_db)):
    if product_id:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı")
        return product
    else:
        products = db.query(Product).all()
        return products


@router.put("/products/{product_id}", response_model=ProductPydantic)
def update_product(product_id: int, updated_product: ProductPydantic, db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.product_id == product_id).first()
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    # Güncelleme işlemi
    existing_product.product_name = updated_product.product_name
    existing_product.category_id = updated_product.category_id
    existing_product.price = updated_product.price
    existing_product.stock_quantity = updated_product.stock_quantity
    existing_product.description = updated_product.description

    db.commit()
    db.refresh(existing_product)
    return existing_product


@router.post("/products/", response_model=ProductPydantic)
def create_product(
    product_name: str, category_id: int, price: float, stock_quantity: int, description: str,
    db: Session = Depends(get_db)
):
    new_product = Product(
        product_name=product_name, category_id=category_id, price=price,
        stock_quantity=stock_quantity, description=description
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Veritabanından ürünü silmek için
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    db.delete(product)
    db.commit()
    return {"message": "Ürün başarıyla silindi"}'''









