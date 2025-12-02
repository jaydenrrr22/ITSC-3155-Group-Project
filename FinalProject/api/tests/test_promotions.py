import pytest
from fastapi import HTTPException
from api.controllers import promotions as crud
from api.schemas.promotions import Promotion, PromotionUpdate

def test_create_promotion(db):
    req = Promotion(
        promotion_name="BOGO",
        description="Buy one get one",
        is_active=True
    )
    item = crud.create(db, req)
    assert item.id is not None

def test_read_all_promotions(db):
    crud.create(db, Promotion(promotion_name="X", description="Desc X", is_active=True))
    crud.create(db, Promotion(promotion_name="Y", description="Desc Y", is_active=False))
    items = crud.read_all(db)
    assert len(items) == 2

def test_read_one_promotion_success(db):
    promo = crud.create(db, Promotion(promotion_name="Z", description="Desc Z", is_active=True))
    found = crud.read_one(db, promo.id)
    assert found.promotion_name == "Z"

def test_read_one_promotion_not_found(db):
    with pytest.raises(HTTPException):
        crud.read_one(db, 999)

def test_update_promotion(db):
    promo = crud.create(db, Promotion(promotion_name="Old", description="Old desc", is_active=True))
    upd = PromotionUpdate(promotion_name="New")
    updated = crud.update(db, promo.id, upd)
    assert updated.promotion_name == "New"

def test_delete_promotion(db):
    promo = crud.create(db, Promotion(promotion_name="Temp", description="Temp promo", is_active=True))
    promo_id = promo.id
    resp = crud.delete(db, promo_id)
    assert resp.status_code == 204

    with pytest.raises(HTTPException):
        crud.read_one(db, promo_id)
