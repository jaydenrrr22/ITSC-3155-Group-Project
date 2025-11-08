from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Payment_information(Base):
    __tablename__ = "payment_information"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_information = Column(String(100), nullable=False)
    transaction_status = Column(String(50), nullable=False)
    payment_type = Column(String(50), nullable=False)
    Payment_information = relationship("payment_information", back_populates="customer")