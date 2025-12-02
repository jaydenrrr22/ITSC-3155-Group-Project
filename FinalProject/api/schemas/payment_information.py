from typing import Optional
from pydantic import BaseModel


class PaymentInfoBase(BaseModel):
    card_information: str
    transaction_status: str
    payment_type: str
    amount: float
    customer_id: int


class PaymentInfoCreate(PaymentInfoBase):
    pass


class PaymentInfoUpdate(BaseModel):
    card_information: Optional[str] = None
    transaction_status: Optional[str] = None
    payment_type: Optional[str] = None
    amount: Optional[float] = None


class PaymentInfo(PaymentInfoBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True