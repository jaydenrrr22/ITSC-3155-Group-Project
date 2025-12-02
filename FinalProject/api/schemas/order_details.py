from typing import Optional
from pydantic import BaseModel
from .menu_items import MenuItem


class OrderDetailBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int
    price: float


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailUpdate(BaseModel):
    quantity: Optional[int] = None
    price: Optional[float] = None
    customer_name: Optional[str] = None
    item_name: Optional[str] = None
    order_status: Optional[str] = None
    order_type: Optional[str] = None
    billing_address: Optional[str] = None
    amount: Optional[float] = None


class StatusUpdate(BaseModel):
    id: int
    order_status: str


class OrderDetail(OrderDetailBase):
    id: Optional[int] = None
    customer_name: Optional[str] = None
    item_name: Optional[str] = None
    order_status: Optional[str] = None
    order_type: Optional[str] = None
    tracking_number: Optional[str] = None
    billing_address: Optional[str] = None
    amount: Optional[float] = None
    menu_items: Optional[MenuItem] = None

    class ConfigDict:
        from_attributes = True