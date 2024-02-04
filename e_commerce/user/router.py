from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from e_commerce.user.model import User
from e_commerce.user.model import UserPydantic

router = APIRouter()


@router.get("/users/")
def read_user(user_id: int = None, db: Session = Depends(get_db)):
    if user_id:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
        return user
    else:
        users = db.query(User).all()
        return users


@router.put("/users/{user_id}", response_model=UserPydantic)
def update_user(user_id: int, updated_user: UserPydantic, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    if updated_user.username is not None:
        existing_user.username = updated_user.username
    if updated_user.address is not None:
        existing_user.address = updated_user.address
    if updated_user.email is not None:
        existing_user.email = updated_user.email

    db.commit()
    db.refresh(existing_user)
    return existing_user


@router.post("/users/", response_model=UserPydantic)
def create_user(
        username: str, address: str, email: str, db: Session = Depends(get_db)
):
    new_user = User(
        username=username, address=address, email=email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User successfully added", "user": new_user}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Veritabanından kullanıcıyı silmek için
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    db.delete(user)
    db.commit()
    return {"message": "Kullanıcı başarıyla silindi"}
