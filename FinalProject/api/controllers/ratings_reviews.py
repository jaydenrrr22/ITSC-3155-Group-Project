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

def update_review_by_id(db, review_id, request):
    try:
        item = db.query(model.RatingsReviews).filter(model.RatingsReviews.id == review_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def delete_review_by_id(db: Session, review_id):
    try:
        item = db.query(model.RatingsReviews).filter(model.RatingsReviews.id == review_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
        return {"message": "Review deleted successfully"}
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

