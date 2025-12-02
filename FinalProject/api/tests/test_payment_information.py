import pytest
from fastapi import HTTPException
from api.controllers import payment_information as crud
from api.schemas.payment_information import PaymentInfo, PaymentInfoUpdate
from api.controllers import customers
from api.schemas.customers import Customer

def setup_customer(db):
    return customers.create(db, Customer(
        customerName="PayUser",
        customerEmail="pay@mail.com",
        customerAddress="road",
        customerPhone="333"
    ))

def test_create_payment_info(db):
    cust = setup_customer(db)
    req = PaymentInfo(
        customer_id=cust.id,
        card_information="1234-5678-9012-3456",
        transaction_status="Pending",
        payment_type="Credit Card",
        amount=99.99
    )
    item = crud.create(db, req)
    assert item.id is not None

def test_read_all_payment_info(db):
    cust = setup_customer(db)
    crud.create(db, PaymentInfo(customer_id=cust.id, card_information="0001", transaction_status="Completed", payment_type="Credit Card", amount=50.00))
    crud.create(db, PaymentInfo(customer_id=cust.id, card_information="0002", transaction_status="Completed", payment_type="Debit Card", amount=75.50))
    items = crud.read_all(db)
    assert len(items) == 2

def test_read_one_payment_info_success(db):
    cust = setup_customer(db)
    info = crud.create(db, PaymentInfo(customer_id=cust.id, card_information="7777", transaction_status="Completed", payment_type="Credit Card", amount=120.00))
    found = crud.read_one(db, info.id)
    assert found.card_information == "7777"

def test_read_one_payment_info_not_found(db):
    with pytest.raises(HTTPException):
        crud.read_one(db, 999)

def test_update_payment_info(db):
    cust = setup_customer(db)
    info = crud.create(db, PaymentInfo(customer_id=cust.id, card_information="123", transaction_status="Pending", payment_type="Credit Card", amount=25.00))
    upd = PaymentInfoUpdate(card_information="0000")
    updated = crud.update(db, info.id, upd)
    assert updated.card_information == "0000"

def test_delete_payment_info(db):
    cust = setup_customer(db)
    info = crud.create(db, PaymentInfo(customer_id=cust.id, card_information="12", transaction_status="Pending", payment_type="Debit Card", amount=10.00))
    info_id = info.id
    resp = crud.delete(db, info_id)
    assert resp.status_code == 204
    with pytest.raises(HTTPException):
        crud.read_one(db, info_id)
