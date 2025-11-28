from typing import Optional, List
from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int
    price: float
    calories: Optional[int] = None
    category: str

class MenuItemsCreation(BaseModel):
    pass

class MenuItemsUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None

class MenuItem(MenuItemBase):
    id: int
    recipe: List["Recipe"] = []

    class Config:
        from_attributes = True

# Resolve forward references
from .recipes import Recipe
MenuItem.update_forward_refs()