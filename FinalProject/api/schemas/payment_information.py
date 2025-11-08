from typing import Optional
from pydantic import BaseModel


class PaymentInformationBase(BaseModel):
    card_information: str
    transaction_status: str
    payment_type: str


class PaymentInformationCreate(PaymentInformationBase):
    pass


class PaymentInformationUpdate(BaseModel):
    card_information: Optional[str] = None
    transaction_status: Optional[str] = None
    payment_type: Optional[str] = None


class Payment_information(PaymentInformationBase):
    id: int

    class ConfigDict:
        from_attributes = True