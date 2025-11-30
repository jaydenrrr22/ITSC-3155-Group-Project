from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models.payment_information import PaymentInformation 
from ..models.menu_items import MenuItem 
from ..models.resources import Resource 
from ..models import order_details 
from ..models.customers import Customers 
from sqlalchemy.exc import SQLAlchemyError 
from datetime import date 
from uuid import uuid4 
def create(db: Session, request): 
    # 1. Fetch payment record for this customer 
    payment = ( 
        db.query(PaymentInformation) 
        .filter(PaymentInformation.customer_id == request.customer_id) 
        .order_by(PaymentInformation.id.desc()) .first() 
        ) 
    if not payment: 
        raise HTTPException( 
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No payment information found for this customer." ) 
    # 2. Validate that customer paid enough 
    if float(payment.amount) < float(request.amount): 
        raise HTTPException( 
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Insufficient funds. Paid: {payment.amount}, order requires: {request.amount}" 
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
            raise HTTPException( 400, f"Not enough {resource.item}. Required: {required}, Available: {resource.amount}" )
        # requres order type to be pickup or delivery 
    if request.type not in ["pickup", "delivery"]: 
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Order type must be either 'pickup' or 'delivery'." ) 
    cust = ( 
        db.query(Customers) 
        .filter(Customers.id == request.customer_id) 
        .order_by(Customers.id.desc()) .first() 
        ) 
    tracking_number = f"TRK-{uuid4().hex[:10].upper()}" 
    desc = request.description 
    type = request.type 
    special = request.special 
    cust_id = request.customer_id 
    menu_id = request.menu_item_id 
    new_item = model.Order( 
        tracking_number=tracking_number, 
        total_amount=menu_item.price, 
        description=desc, 
        billing_address=cust.customerAddress, 
        type=type, 
        order_status="pending", 
        special=special, 
        customer_id= cust_id, 
        menu_item_id=menu_id 
        ) 
    try: 
        db.add(new_item) 
        db.commit() 
        db.refresh(new_item) 
        new_detail = order_details.OrderDetail( 
            order_id=new_item.id, 
            menu_item_id=menu_id, 
            customer_name=cust.customerName, 
            item_name=menu_item.name, 
            order_status="pending", 
            order_type=type, 
            tracking_number=tracking_number, 
            amount=menu_item.price, 
            billing_address=cust.customerAddress 
            ) 
        try: 
            db.add(new_detail) 
            db.commit() 
            db.refresh(new_detail) 
        except SQLAlchemyError as e: 
            error = str(e.__dict__['orig']) 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error) 
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
