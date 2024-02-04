from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from e_commerce.orderitem.model import OrderItem
from e_commerce.orderitem.model import OrderItemPydantic

router = APIRouter()

@router.get("/orderitems/")
def read_orderitems(orderitem_id: int = None, db: Session = Depends(get_db)):
    if orderitem_id:
        orderitem = db.query(OrderItem).filter(OrderItem.detail_id == orderitem_id).first()
        if orderitem is None:
            raise HTTPException(status_code=404, detail="Sipariş öğesi bulunamadı")
        return orderitem
    else:
        orderitems = db.query(OrderItem).all()
        return orderitems

@router.put("/orderitems/{orderitem_id}", response_model=OrderItemPydantic)
def update_orderitem(orderitem_id: int, updated_orderitem: OrderItemPydantic, db: Session = Depends(get_db)):
    existing_orderitem = db.query(OrderItem).filter(OrderItem.detail_id == orderitem_id).first()
    if existing_orderitem is None:
        raise HTTPException(status_code=404, detail="Sipariş öğesi bulunamadı")

    # Güncelleme işlemi
    existing_orderitem.order_id = updated_orderitem.order_id
    existing_orderitem.product_id = updated_orderitem.product_id
    existing_orderitem.subtotal = updated_orderitem.subtotal

    db.commit()
    db.refresh(existing_orderitem)
    return existing_orderitem

@router.post("/orderitems/", response_model=OrderItemPydantic)
def create_orderitem(
    order_id: int, product_id: int, subtotal: float,
    db: Session = Depends(get_db)
):
    new_orderitem = OrderItem(
        order_id=order_id, product_id=product_id, subtotal=subtotal
    )
    db.add(new_orderitem)
    db.commit()
    db.refresh(new_orderitem)
    return new_orderitem

@router.delete("/orderitems/{orderitem_id}")
def delete_orderitem(orderitem_id: int, db: Session = Depends(get_db)):
    # Veritabanından sipariş öğesini silmek için
    orderitem = db.query(OrderItem).filter(OrderItem.detail_id == orderitem_id).first()
    if orderitem is None:
        raise HTTPException(status_code=404, detail="Sipariş öğesi bulunamadı")

    db.delete(orderitem)
    db.commit()
    return {"message"}
