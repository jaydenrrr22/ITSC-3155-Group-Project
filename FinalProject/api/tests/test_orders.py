import pytest
from unittest.mock import Mock
from ..controllers import orders as controller
from ..models import orders as order_model, payment_information as payment_model
from ..models import menu_items as menu_model, resources as resource_model

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def mock_payment(customer_id=1, amount=100):
    payment = Mock(spec=payment_model.PaymentInformation)
    payment.customer_id = customer_id
    payment.amount = amount
    return payment

def mock_menu_item(menu_item_id=1, recipe_amount=1, resource_amount=10):
    # Mock resource
    resource = Mock(spec=resource_model.Resource)
    resource.id = 1
    resource.item = "Cheese"
    resource.amount = resource_amount

    # Mock recipe
    recipe = Mock()
    recipe.resource_id = resource.id
    recipe.amount = recipe_amount
    recipe.resource = resource

    # Mock menu item
    menu_item = Mock(spec=menu_model.MenuItem)
    menu_item.id = menu_item_id
    menu_item.recipes = [recipe]

    return menu_item, resource

def test_create_order_success(db_session):
    # Arrange
    order_request = Mock()
    order_request.customer_id = 1
    order_request.total_amount = 50
    order_request.menu_item_id = 1
    order_request.amount = 2
    order_request.tracking_number = 123
    order_request.order_status = "waiting"
    order_request.order_date = "2025-11-29T23:52:53.933Z"
    order_request.description = "Test order"
    order_request.billing_address = "123 Street"

    # Mock DB queries
    payment = mock_payment(amount=100)
    menu_item, resource = mock_menu_item(resource_amount=10)

    db_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = payment
    db_session.query.return_value.filter.return_value.first.return_value = menu_item
    db_session.query.return_value.filter.return_value.first.side_effect = [menu_item, resource]

    # Act
    created_order = controller.create(db_session, order_request)

    # Assert
    assert created_order is not None
    assert created_order.tracking_number == 123
    assert created_order.order_status == "waiting"


def test_create_order_no_payment(db_session):
    order_request = Mock()
    order_request.customer_id = 1
    order_request.total_amount = 50
    order_request.menu_item_id = 1
    order_request.amount = 2

    db_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = None

    import pytest
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        controller.create(db_session, order_request)

    assert exc_info.value.status_code == 400
    assert "No payment information" in exc_info.value.detail


def test_create_order_insufficient_payment(db_session):
    order_request = Mock()
    order_request.customer_id = 1
    order_request.total_amount = 100
    order_request.menu_item_id = 1
    order_request.amount = 1

    payment = mock_payment(amount=50)
    db_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = payment

    import pytest
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        controller.create(db_session, order_request)

    assert exc_info.value.status_code == 400
    assert "Insufficient funds" in exc_info.value.detail


def test_create_order_insufficient_resources(db_session):
    order_request = Mock()
    order_request.customer_id = 1
    order_request.total_amount = 10
    order_request.menu_item_id = 1
    order_request.amount = 5

    payment = mock_payment(amount=100)
    menu_item, resource = mock_menu_item(resource_amount=2)  # Not enough resource

    db_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = payment
    db_session.query.return_value.filter.return_value.first.side_effect = [menu_item, resource]

    import pytest
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        controller.create(db_session, order_request)

    assert exc_info.value.status_code == 400
    assert "Not enough" in exc_info.value.detail


def test_create_order_menu_item_not_found(db_session):
    order_request = Mock()
    order_request.customer_id = 1
    order_request.total_amount = 10
    order_request.menu_item_id = 999  # Nonexistent
    order_request.amount = 1

    payment = mock_payment(amount=100)
    db_session.query.return_value.filter.return_value.order_by.return_value.first.return_value = payment
    db_session.query.return_value.filter.return_value.first.return_value = None

    import pytest
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        controller.create(db_session, order_request)

    assert exc_info.value.status_code == 404
    assert "Menu item" in exc_info.value.detail
