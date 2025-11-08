from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import ratings_reviews as controller
from ..schemas import ratings_reviews as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['RatingsReviews'],
    prefix="/ratings_reviews",
)

@router.post("/", response_model=schema.ratings_reviews)
def create(request: schema.ratings_reviewsCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)
