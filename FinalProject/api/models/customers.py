from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Customers(Base):
    __tablename__ = "Customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customerName = Column(String(100), nullable=False)
    customerEmail = Column(String(100), nullable=False, unique=True)
    customerPhone = Column(String(100), nullable=False, unique=True)
    customerAddress = Column(String(100), nullable=False)

    orders = relationship("Order", back_populates="customer")


