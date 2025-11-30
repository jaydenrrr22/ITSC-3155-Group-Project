from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # tracking number for order (store as string to allow prefixed values)
    tracking_number = Column(String(50), unique=True, nullable=False)
    # Status: e.g., "Pending", "Preparing", "Completed"
    order_status = Column(String(100), nullable=False, default="pending")
    # Total price of the order
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(String(300))
    billing_address = Column(String(200))
    type = Column(String(50), default="pickup")
    special = Column(String(200))
    # Relationship to Customer (if Customer table exists)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    # Use string reference here to avoid circular import
    customer = relationship("Customers", back_populates="orders")

    order_details = relationship("OrderDetail", back_populates="order")
    promotions = relationship("Promotions", back_populates="order")

