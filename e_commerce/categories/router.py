from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from e_commerce.categories.model import CategoryPydantic
from e_commerce.categories.model import Category
from e_commerce.product.model import Product


from models import get_db


router = APIRouter()


@router.get("/categories/")
def read_categories(category_id: int = None, db: Session = Depends(get_db)):
    if category_id:
        category = db.query(Category).filter(Category.category_id == category_id).first()
        if category is None:
            raise HTTPException(status_code=404, detail="Kategori bulunamadı")
        return category
    else:
        categories = db.query(Category).all()# tüm kayıtları veritabanından çeker ve bir listeler
        return categories


@router.put("/categories/{category_id}", response_model=CategoryPydantic)
def update_category(category_id: int, updated_category: CategoryPydantic, db: Session = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.category_id == category_id).first()
    if existing_category is None:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")

    existing_category.category_name= updated_category.category_name
    existing_category.category_type = updated_category.category_type

    db.commit()
    db.refresh(existing_category)
    return existing_category


@router.post("/categories/", response_model=CategoryPydantic)
def create_category(category_name: str, category_type: str, db: Session = Depends(get_db)):
    new_category = Category(category_name=category_name, category_type=category_type)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if category:

        products = db.query(Product).filter(Product.category_id == category_id).all()


        for product in products:
            db.delete(product)


        db.delete(category)
        db.commit() #işlemi onaylayan bir metod.kalıcı hale getirir

        return {"message": "Category and associated products deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Category not found")#hata durumu oluşturur.
    db.query(Product).filter(Product.category_id == category_id).delete()


