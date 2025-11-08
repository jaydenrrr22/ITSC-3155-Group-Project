from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    traking_number = Column(String(30), unique=True, nullable=False)
    order_status = Column(String(100), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    order_details = relationship("OrderDetail", back_populates="order")

    promotions = relationship("Promotions", back_populates="order")
    #customer_name = Column(String(100), ForeignKey("Customers.customerName"))
    billing_address = Column(String(200))
    customer = relationship("Customer", back_populates="orders")
    customer_name = Column(String(200), nullable=False)