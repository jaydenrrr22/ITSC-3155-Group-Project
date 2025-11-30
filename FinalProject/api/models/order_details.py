from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=True)
    tracking_number = Column(String(150), nullable=False)
    customer_name = Column(String(150), nullable=False)
    item_name = Column(String(150), nullable=False)
    order_status = Column(String(100), nullable=False)
    order_type = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    billing_address = Column(String(200))

    order = relationship("Order", back_populates="order_details")
    menu_item = relationship("MenuItem", back_populates="order_details")
