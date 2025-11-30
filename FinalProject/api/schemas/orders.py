from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail



class OrderBase(BaseModel):
    tracking_number: str
    order_status: str
    total_amount: float
    order_date: datetime
    description: Optional[str] = None
    billing_address: Optional[str] = None
    customer_id: int
    type: str = "pickup"
    special: Optional[str] = None



class OrderCreate(BaseModel):
    customer_id: int
    menu_item_id: int
    amount: int = 1
    description: Optional[str] = None
    type: str = "pickup"
    special: Optional[str] = None


class OrderUpdate(BaseModel):
    tracking_number: Optional[int] = None
    order_status: Optional[str] = None
    total_amount: Optional[float] = None
    description: Optional[str] = None
    billing_address: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: datetime
    order_details: List[OrderDetail] = []

    class ConfigDict:
        from_attributes = True