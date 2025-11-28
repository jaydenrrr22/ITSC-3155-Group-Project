from typing import Optional
from pydantic import BaseModel, condecimal


class PaymentInformationBase(BaseModel):
    card_information: str
    transaction_status: str
    payment_type: str
    amount: float
    customer_id: int



class PaymentInformationCreate(PaymentInformationBase):
    pass


class PaymentInformationUpdate(BaseModel):
    card_information: Optional[str] = None
    transaction_status: Optional[str] = None
    payment_type: Optional[str] = None
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None


class PaymentInformation(PaymentInformationBase):
    id: int
    customer_id: int

    class ConfigDict:
        from_attributes = True