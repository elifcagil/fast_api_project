from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from e_commerce.orders.model import Orders
from e_commerce.orders.model import OrdersPydantic
from e_commerce.user.model import User
from e_commerce.user.model import UserPydantic

router = APIRouter()


@router.get("/orders/")
def read_orders(order_id: int = None, db: Session = Depends(get_db)):
    if order_id:
        order = db.query(Orders).filter(Orders.orders_id == order_id).first()
        if order is None:
            raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
        return order
    else:
        orders = db.query(Orders).all()
        return orders


@router.put("/orders/{order_id}", response_model=OrdersPydantic)
def update_order(order_id: int, updated_order: OrdersPydantic, db: Session = Depends(get_db)):
    existing_order = db.query(Orders).filter(Orders.orders_id == order_id).first()
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")


    existing_order.orders_date = updated_order.orders_date
    existing_order.customer_id = updated_order.user_id
    existing_order.quantity = updated_order.quantity
    existing_order.subtotal = updated_order.subtotal
    existing_order.unitprice = updated_order.unitprice
    existing_order.total_amount = updated_order.total_amount

    db.commit()
    db.refresh(existing_order)
    return existing_order


@router.post("/orders/", response_model=OrdersPydantic)
def create_order(
    orders_date: str, user_id: int, quantity: int, subtotal: float, unitprice: float, total_amount: float,
    db: Session = Depends(get_db)
):
    new_order = Orders(
        orders_date=orders_date, customer_id=user_id, quantity=quantity,
        subtotal=subtotal, unitprice=unitprice, total_amount=total_amount
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    # Veritabanından siparişi silmek için
    order = db.query(Orders).filter(Orders.orders_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")

    db.delete(order)
    db.commit()
    return {"message": "Sipariş başarıyla silindi"}
