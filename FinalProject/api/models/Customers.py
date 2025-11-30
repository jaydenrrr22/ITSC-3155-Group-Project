from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customerName = Column(String(100), nullable=False)
    customerEmail = Column(String(100), nullable=False, unique=True)
    customerPhone = Column(String(100), nullable=False, unique=True)
    customerAddress = Column(String(100), nullable=False)

    orders = relationship("Order", back_populates="customer")
    reviews = relationship("RatingsReviews", back_populates="customer")
    payments = relationship("PaymentInformation", back_populates="customer")

