from pydantic import BaseModel, condecimal
from typing import Optional

class RatingReviewBase(BaseModel):
    reviewText: str
    ratingScore: condecimal(max_digits=2, decimal_places=1)
    customer_id: Optional[int] = None  # optional if not passed directly
    menu_item_id: int


class RatingReviewCreate(RatingReviewBase):
    pass


class RatingReview(RatingReviewBase):
    id: int

    class Config:
        orm_mode = True  # allows reading SQLAlchemy objects directly

class RatingReviewUpdate(BaseModel):
    reviewText: Optional[str] = None
    ratingScore: Optional[condecimal(max_digits=2, decimal_places=1)] = None

    class Config:
        from_attribute = True
