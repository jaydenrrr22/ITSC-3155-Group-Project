from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .menu_items import MenuItem


class OrderDetailBase(BaseModel):
    amount: int


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    menu_items_id: int

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_items_id: Optional[int] = None
    amount: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    menu_items: MenuItem = Optional[MenuItem]

    class ConfigDict:
        from_attributes = True