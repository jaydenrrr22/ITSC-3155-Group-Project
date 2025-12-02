from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import order_details as model
from ..models.menu_items import MenuItem
from ..models.customers import Customers
from ..models.orders import Order
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    order = (
        db.query(Order)
        .filter(Order.id == request.order_id)
        .order_by(Order.id.desc())
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No order found for this order ID."
        )
    
    item = (
        db.query(MenuItem)
        .filter(MenuItem.id == request.menu_item_id)
        .order_by(MenuItem.id.desc())
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No menu item found for this menu item ID."
        )
    
    customer = (
        db.query(Customers)
        .filter(Customers.id == order.customer_id)
        .order_by(Customers.id.desc())
        .first()
    )

    new_item = model.OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        customer_name=customer.customerName,
        item_name=item.name,
        order_status=order.order_status,
        order_type=order.type,
        billing_address=order.billing_address,
        tracking_number=order.tracking_number,
        amount=(request.quantity * request.price)
    )
    # Attach transient attributes for API consumers/tests (not persisted fields)
    try:
        new_item.quantity = request.quantity
        new_item.price = request.price
    except Exception:
        pass

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def update_status(db: Session, id: int):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.update({"order_status": "Completed"}, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def read_one(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.model_dump(exclude_unset=True, exclude_none=True)
        # Remove transient fields that aren't columns in the DB
        update_data.pop('quantity', None)
        update_data.pop('price', None)
        if not update_data:
            return item.first()
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
