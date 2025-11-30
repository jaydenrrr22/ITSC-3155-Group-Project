from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .menu_items import MenuItem


class OrderDetailBase(BaseModel):
    order_id: int
    menu_item_id: int
    customer_name: str
    item_name: str
    order_status: str
    order_type: str
    tracking_number: str
    billing_address: str
    amount: int


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    menu_item_id: int

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    customer_id: Optional[int] = None
    amount: Optional[int] = None

class StatusUpdate(BaseModel):
    id: int
    order_status: str

class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    menu_items: MenuItem = Optional[MenuItem]

    class ConfigDict:
        from_attributes = True