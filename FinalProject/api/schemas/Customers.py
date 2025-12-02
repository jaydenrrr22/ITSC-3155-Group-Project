from typing import Optional, List
from pydantic import BaseModel

# Base schema shared between Create and Read
class CustomerBase(BaseModel):
    customerName: str
    customerEmail: str
    customerPhone: str
    customerAddress: str


# Schema used when creating a customer (request body)
class CustomerCreate(CustomerBase):
    pass

# Schema used when updating a customer (request body)
class CustomerUpdate(BaseModel):
    customerName: Optional[str] = None
    customerEmail: Optional[str] = None
    customerPhone: Optional[str] = None
    customerAddress: Optional[str] = None

# Schema used when returning a customer from the API
class Customer(CustomerBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True