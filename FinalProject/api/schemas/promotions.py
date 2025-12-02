from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PromotionBase(BaseModel):
    promotion_name: str
    description: Optional[str] = None
    order_id: Optional[int] = None
    expiration_date: Optional[datetime] = None
    is_active: Optional[bool] = True


class PromotionCreate(PromotionBase):
    """Used when creating a new promotion"""
    pass


class PromotionUpdate(BaseModel):
    """Used when updating a promotion"""
    promotion_name: Optional[str] = None
    description: Optional[str] = None
    expiration_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class Promotion(PromotionBase):
    """Returned in responses"""
    id: Optional[int] = None
    generate_date: Optional[datetime] = None

    # ✅ Pydantic v2 replacement for orm_mode
    model_config = {
        "from_attributes": True
    }

