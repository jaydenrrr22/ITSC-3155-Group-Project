from typing import List

from fastapi import APIRouter, Depends, FastAPI, status, Response, HTTPException
from sqlalchemy.engine import row
from sqlalchemy.orm import Session
from ..controllers import ratings_reviews as controller
from ..controllers import menu_items as menu_item_controller
from ..schemas import ratings_reviews as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['RatingsReviews'],
    prefix="/ratings_reviews",
)

@router.post("/", response_model=schema.RatingReview)
def create(request: schema.RatingReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/complaints")
def get_bad_reviews(db: Session = Depends(get_db)):
    complaints = controller.get_complaints(db=db)

    if not complaints:
        return { "message": "No complaints found" }

    return [
        {
            "menu_item": row.name,
            "score": row[0].ratingScore,
            "complaints": row[0].reviewText
        }
        for row in complaints
    ]

@router.get("/reviews/{menu_item_id}", response_model=List[schema.RatingReview])
def get_reviews_by_menu_id(menu_item_id: int, db: Session = Depends(get_db)):
    try:
        menu_item_controller.read_one(db, item_id=menu_item_id)
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Item with {menu_item_id} does not exist")
        raise e

    reviews = controller.get_reviews_by_menu_item_id(db, menu_item_id)

    if not reviews:
        raise HTTPException(status_code=404, detail = "No reviews found")

    return controller.get_reviews_by_menu_item_id(db, menu_item_id)