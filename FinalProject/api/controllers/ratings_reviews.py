from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import ratings_reviews as model
from ..models.menu_items import MenuItem
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.RatingsReviews(
        reviewText=request.reviewText,
        ratingScore=request.ratingScore,
        customer_id=request.customer_id,
        menu_item_id=request.menu_item_id,
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

def get_complaints(db: Session):
    result = (
        db.query(model.RatingsReviews, MenuItem.name)
        .join(MenuItem, MenuItem.id == model.RatingsReviews.menu_item_id)
        .filter(model.RatingsReviews.ratingScore < 3)
        .all()
    )
    return result

def get_reviews_by_menu_item_id(db: Session, menu_item_id: int):
    result = (
        db.query(model.RatingsReviews)
        .filter(model.RatingsReviews.menu_item_id == menu_item_id)
        .all()
    )

    return result