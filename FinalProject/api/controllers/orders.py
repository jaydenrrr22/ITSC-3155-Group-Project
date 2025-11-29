from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models.payment_information import PaymentInformation
from ..models.menu_items import MenuItem
from ..models.resources import Resource
from sqlalchemy.exc import SQLAlchemyError
from datetime import date


def create(db: Session, request):
    # 1. Fetch payment record for this customer
    payment = (
        db.query(PaymentInformation)
        .filter(PaymentInformation.customer_id == request.customer_id)
        .order_by(PaymentInformation.id.desc())
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No payment information found for this customer."
        )

    # 2. Validate that customer paid enough
    if float(payment.amount) < float(request.total_amount):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient funds. Paid: {payment.amount}, order requires: {request.total_amount}"
        )

    # Check resource inventory for each menu item requested
    menu_item = (
        db.query(MenuItem)
        .filter(MenuItem.id == request.menu_item_id)
        .first()
    )
    if not menu_item:
        raise HTTPException(404, f"Menu item {request.menu_item_id} not found")

    # Each menu item requires recipes (ingredients)
    for recipe in menu_item.recipes:
        resource = db.query(Resource).filter(Resource.id == recipe.resource_id).first()

        required = recipe.amount * request.amount

        if resource.amount < required:
            raise HTTPException(
                400,
                f"Not enough {resource.item}. Required: {required}, Available: {resource.amount}"
            )

    new_item = model.Order(
        tracking_number=request.tracking_number,
        order_status=request.order_status,
        total_amount=request.total_amount,
        order_date=request.order_date,
        description=request.description,
        billing_address=request.billing_address,
        customer_id=request.customer_id
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session, start_date: date=None, end_date: date=None):
    try:
        query = db.query(model.Order)

        # If both dates are provided → filter by range
        if start_date and end_date:
            query = query.filter(model.Order.order_date >= start_date, model.Order.order_date <= end_date)

        result = query.all()

        return result
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
