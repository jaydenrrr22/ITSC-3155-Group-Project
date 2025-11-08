from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Promotions(Base):
    __tablename__ = "promotions"

    # Primary key for promotions
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Promotion info
    promotion_name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)  # optional description
    
    # Link to an order (optional, can be nullable if promotion not tied to a single order)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)

    # Dates with timezone-aware datetimes
    generate_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    expiration_date = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # Active flag
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Promotion(id={self.id}, name={self.promotion_name}, active={self.is_active})>"




    