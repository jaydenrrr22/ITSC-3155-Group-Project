from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class RatingsReviews(Base):
    __tablename__ = "RatingsReviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reviewText = Column(String(100), nullable=False, unique=False)
    ratingScore = Column(DECIMAL(1,1), nullable=False, unique=False)

    customers = relationship("customer", back_populates="reviews")