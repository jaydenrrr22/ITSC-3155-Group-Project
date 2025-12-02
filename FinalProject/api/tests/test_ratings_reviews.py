import pytest
from fastapi import HTTPException
from api.controllers import ratings_reviews as crud
from api.schemas.ratings_reviews import RatingReview, RatingReviewUpdate
from api.controllers import customers, menu_items
from api.schemas.customers import Customer
from api.schemas.menu_items import MenuItem

def setup_nested(db):
    cust = customers.create(db, Customer(
        customerName="Reviewer",
        customerEmail="rev@mail.com",
        customerAddress="L",
        customerPhone="90"
    ))
    item = menu_items.create(db, MenuItem(
        name="Cake",
        description="Sweet",
        quantity=10,
        price=4.00,
        category="Dessert"
    ))
    return cust, item

def test_create_rating_review(db):
    cust, item = setup_nested(db)
    req = RatingReview(
        customer_id=cust.id,
        menu_item_id=item.id,
        ratingScore=5,
        reviewText="Excellent"
    )
    r = crud.create(db, req)
    assert r.id is not None

def test_read_all_rating_reviews(db):
    cust, item = setup_nested(db)
    crud.create(db, RatingReview(customer_id=cust.id, menu_item_id=item.id, ratingScore=4, reviewText="Good"))
    crud.create(db, RatingReview(customer_id=cust.id, menu_item_id=item.id, ratingScore=3, reviewText="OK"))
    items = crud.get_reviews_by_menu_item_id(db, item.id)
    assert len(items) >= 2

def test_read_one_rating_review_success(db):
    cust, item = setup_nested(db)
    r = crud.create(db, RatingReview(customer_id=cust.id, menu_item_id=item.id, ratingScore=4, reviewText="Nice"))
    found = crud.get_reviews_by_menu_item_id(db, item.id)
    assert len(found) > 0 and found[0].ratingScore == 4

def test_read_one_rating_review_not_found(db):
    # get_reviews_by_menu_item_id returns an empty list for non-existent menu items
    result = crud.get_reviews_by_menu_item_id(db, 999)
    assert len(result) == 0

def test_update_rating_review(db):
    cust, item = setup_nested(db)
    r = crud.create(db, RatingReview(customer_id=cust.id, menu_item_id=item.id, ratingScore=2, reviewText="Bad"))
    upd = RatingReviewUpdate(ratingScore=5)
    updated = crud.update_review_by_id(db, r.id, upd)
    assert updated.ratingScore == 5

def test_delete_rating_review(db):
    cust, item = setup_nested(db)
    r = crud.create(db, RatingReview(customer_id=cust.id, menu_item_id=item.id, ratingScore=3, reviewText="Mid"))
    r_id = r.id
    resp = crud.delete_review_by_id(db, r_id)
    assert resp["message"] == "Review deleted successfully"
