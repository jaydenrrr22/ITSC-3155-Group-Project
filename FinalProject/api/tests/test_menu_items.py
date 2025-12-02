import pytest
from fastapi import HTTPException
from api.controllers import menu_items as crud
from api.schemas.menu_items import MenuItem, MenuItemUpdate

def test_create_menu_item(db):
    req = MenuItem(
        name="Burger",
        description="Tasty",
        quantity=10,
        price=10.99,
        category="Sandwich"
    )
    item = crud.create(db, req)
    assert item.id is not None
    assert item.name == "Burger"

def test_read_all_menu_items(db):
    crud.create(db, MenuItem(name="A", description="x", quantity=5, price=5.00, category="Sides"))
    crud.create(db, MenuItem(name="B", description="y", quantity=6, price=6.00, category="Drinks"))
    items = crud.read_all(db)
    assert len(items) == 2

def test_read_one_menu_item_success(db):
    item = crud.create(db, MenuItem(name="Soup", description="Hot", quantity=4, price=4.50, category="Soups"))
    result = crud.read_one(db, item.id)
    assert result.name == "Soup"

def test_read_one_menu_item_not_found(db):
    with pytest.raises(HTTPException):
        crud.read_one(db, 999)

def test_update_menu_item(db):
    item = crud.create(db, MenuItem(name="Old", description="Z", quantity=1, price=1.00, category="Other"))
    upd = MenuItemUpdate(name="New")
    result = crud.update(db, item.id, upd)
    assert result.name == "New"

def test_delete_menu_item(db):
    item = crud.create(db, MenuItem(name="Temp", description="x", quantity=2, price=2.00, category="Other"))
    item_id = item.id
    resp = crud.delete(db, item_id)
    assert resp.status_code == 204

    with pytest.raises(HTTPException):
        crud.read_one(db, item_id)
