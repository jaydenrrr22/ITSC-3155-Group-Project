from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import ratings_reviews as model
from ..models.sandwiches import Sandwich
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.RatingsReviews(
        reviewText=request.reviewText,
        ratingScore=request.ratingScore,
        customer_id=request.customer_id,
        sandwich_id=request.sandwich_id
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

def get_reviews(db: Session):
    result = (
        db.query(model.RatingsReviews, Sandwich.sandwich_name)
        .join(Sandwich, Sandwich.id == model.RatingsReviews.sandwich_id)
        .filter(model.RatingsReviews.ratingScore < 3)
        .all()
    )
    return result