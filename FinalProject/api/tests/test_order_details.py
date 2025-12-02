import pytest
from fastapi import HTTPException
from api.controllers import order_details as crud
from api.controllers import orders, customers, menu_items, payment_information
from api.schemas.order_details import OrderDetail, OrderDetailUpdate
from api.schemas.customers import Customer
from api.schemas.menu_items import MenuItem
from api.schemas.payment_information import PaymentInfo
from api.schemas.orders import OrderCreate

def setup_dependencies(db):
    cust = customers.create(db, Customer(
        customerName="C",
        customerEmail="c@mail.com",
        customerAddress="here",
        customerPhone="000"
    ))
    item = menu_items.create(db, MenuItem(
        name="Taco",
        description="Hot",
        quantity=10,
        price=3.00,
        category="Tacos"
    ))
    # create payment info for this customer so orders can be created
    payment_information.create(db, PaymentInfo(
        customer_id=cust.id,
        card_information="0000-0000-0000-0000",
        transaction_status="Completed",
        payment_type="Test",
        amount=10.00
    ))
    order = orders.create(db, OrderCreate(
        customer_id=cust.id,
        menu_item_id=item.id,
        amount=2,
        type="pickup"
    ))
    return cust, item, order

def test_create_order_detail(db):
    cust, item, order = setup_dependencies(db)
    req = OrderDetail(
        order_id=order.id,
        menu_item_id=item.id,
        quantity=2,
        price=6
    )
    detail = crud.create(db, req)
    assert detail.id is not None
    assert detail.order_id == order.id

def test_read_all_order_details(db):
    cust, item, order = setup_dependencies(db)
    crud.create(db, OrderDetail(order_id=order.id, menu_item_id=item.id, quantity=1, price=3))
    crud.create(db, OrderDetail(order_id=order.id, menu_item_id=item.id, quantity=2, price=6))
    items = crud.read_all(db)
    assert len(items) >= 2

def test_read_one_order_detail_success(db):
    cust, item, order = setup_dependencies(db)
    d = crud.create(db, OrderDetail(order_id=order.id, menu_item_id=item.id, quantity=1, price=3))
    result = crud.read_one(db, d.id)
    assert result.quantity == 1

def test_read_one_order_detail_not_found(db):
    with pytest.raises(HTTPException):
        crud.read_one(db, 999)

def test_update_order_detail(db):
    cust, item, order = setup_dependencies(db)
    d = crud.create(db, OrderDetail(order_id=order.id, menu_item_id=item.id, quantity=1, price=3))
    upd = OrderDetailUpdate(customer_name="Updated")
    result = crud.update(db, d.id, upd)
    assert result.customer_name == "Updated"

def test_delete_order_detail(db):
    cust, item, order = setup_dependencies(db)
    d = crud.create(db, OrderDetail(order_id=order.id, menu_item_id=item.id, quantity=1, price=3))
    d_id = d.id
    resp = crud.delete(db, d_id)
    assert resp.status_code == 204
    with pytest.raises(HTTPException):
        crud.read_one(db, d_id)
