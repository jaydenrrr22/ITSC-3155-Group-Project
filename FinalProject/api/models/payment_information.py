from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class PaymentInformation(Base):
    __tablename__ = "payment_information"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_information = Column(String(100), nullable=False)
    transaction_status = Column(String(50), nullable=False)
    payment_type = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customers", back_populates="payments")
