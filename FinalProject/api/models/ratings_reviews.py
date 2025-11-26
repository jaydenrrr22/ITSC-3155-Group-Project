from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class RatingsReviews(Base):
    __tablename__ = "ratings_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reviewText = Column(String(100), nullable=False)
    ratingScore = Column(DECIMAL(2, 1), nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customers", back_populates="reviews")

    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    menu_item = relationship("MenuItem", back_populates="reviews")