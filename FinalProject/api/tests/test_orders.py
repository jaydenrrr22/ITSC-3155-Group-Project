import pytest
from fastapi import HTTPException
from api.controllers import orders as crud
from api.controllers import customers, menu_items
from api.schemas.orders import OrderCreate, OrderUpdate
from api.schemas.customers import Customer
from api.schemas.menu_items import MenuItem

def setup_related(db):
    cust = customers.create(db, Customer(
        customerName="Zed",
        customerEmail="z@mail.com",
        customerAddress="x",
        customerPhone="123"
    ))
    item = menu_items.create(db, MenuItem(
        name="Pizza",
        description="Cheese",
        quantity=5,
        price=12.00,
        category="Pizza"
    ))
    # ensure customer has payment info for order creation
    from api.schemas.payment_information import PaymentInfo
    from api.controllers import payment_information as payments
    payments.create(db, PaymentInfo(
        customer_id=cust.id,
        card_information="1111-2222-3333-4444",
        transaction_status="Completed",
        payment_type="Test",
        amount=10.00
    ))
    return cust, item

def test_create_order(db):
    cust, item = setup_related(db)
    req = OrderCreate(
        customer_id=cust.id,
        menu_item_id=item.id,
        amount=1,
        type="delivery"
    )
    order = crud.create(db, req)
    assert order.id is not None
    assert order.customer_id == cust.id

def test_read_all_orders(db):
    cust, item = setup_related(db)
    crud.create(db, OrderCreate(customer_id=cust.id, menu_item_id=item.id, amount=1, type="pickup"))
    crud.create(db, OrderCreate(customer_id=cust.id, menu_item_id=item.id, amount=2, type="pickup"))
    items = crud.read_all(db, None, None)
    assert len(items) == 2

def test_read_one_order_success(db):
    cust, item = setup_related(db)
    order = crud.create(db, OrderCreate(customer_id=cust.id, menu_item_id=item.id, amount=3, type="pickup"))
    found = crud.read_one(db, order.id)
    # Order total_amount is set to menu_item.price (12.00), not request.amount
    assert found.total_amount == item.price

def test_read_one_order_not_found(db):
    with pytest.raises(HTTPException):
        crud.read_one(db, 999)

def test_update_order(db):
    cust, item = setup_related(db)
    order = crud.create(db, OrderCreate(customer_id=cust.id, menu_item_id=item.id, amount=1, type="pickup"))
    upd = OrderUpdate(total_amount=9)
    updated = crud.update(db, order.id, upd)
    assert updated.total_amount == 9

def test_delete_order(db):
    cust, item = setup_related(db)
    order = crud.create(db, OrderCreate(customer_id=cust.id, menu_item_id=item.id, amount=1, type="pickup"))
    order_id = order.id
    resp = crud.delete(db, order_id)
    assert resp.status_code == 204
    with pytest.raises(HTTPException):
        crud.read_one(db, order_id)
