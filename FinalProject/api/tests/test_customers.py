import pytest
from fastapi import HTTPException
from api.controllers import customers as crud
from api.schemas.customers import Customer, CustomerUpdate

def test_create_customer(db):
    req = Customer(
        customerName="John",
        customerEmail="john@example.com",
        customerAddress="123 Street",
        customerPhone="555-1111"
    )
    item = crud.create(db, req)
    assert item.id is not None
    assert item.customerName == "John"

def test_read_all_customers(db):
    for x in range(2):
        crud.create(db, Customer(
            customerName=f"User{x}",
            customerEmail=f"u{x}@test.com",
            customerAddress="A",
            customerPhone=f"P{x}"
        ))
    items = crud.read_all(db)
    assert len(items) == 2

def test_read_one_customer_success(db):
    item = crud.create(db, Customer(
        customerName="A",
        customerEmail="a@b.com",
        customerAddress="X",
        customerPhone="Z"
    ))
    result = crud.read_one(db, item.id)
    assert result.customerName == "A"

def test_read_one_customer_not_found(db):
    with pytest.raises(HTTPException) as e:
        crud.read_one(db, 999)
    assert e.value.status_code == 404

def test_update_customer(db):
    item = crud.create(db, Customer(
        customerName="A",
        customerEmail="x@y.com",
        customerAddress="T",
        customerPhone="UP1"
    ))
    upd = CustomerUpdate(customerName="NewName")
    result = crud.update(db, item.id, upd)
    assert result.customerName == "NewName"

def test_delete_customer(db):
    item = crud.create(db, Customer(
        customerName="Del",
        customerEmail="d@e.com",
        customerAddress="S",
        customerPhone="T"
    ))
    item_id = item.id
    resp = crud.delete(db, item_id)
    assert resp.status_code == 204
    with pytest.raises(HTTPException):
        crud.read_one(db, item_id)
