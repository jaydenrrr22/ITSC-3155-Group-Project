from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import ratings_reviews as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['RatingsReviews'],
    prefix="/ratings_reviews",
)
