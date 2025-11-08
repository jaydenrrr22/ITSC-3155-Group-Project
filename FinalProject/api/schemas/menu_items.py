from typing import Optional, List
from pydantic import BaseModel
from .recipes import Recipe

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    calories: Optional[int] = None
    category: str

class MenuItemsCreation(BaseModel):
    pass

class MenuItemsUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None

class MenuItem(MenuItemBase):
    id: int
    recipe: List[Recipe] = []

    class Config:
        from_attributes = True