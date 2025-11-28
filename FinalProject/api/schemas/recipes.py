from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .resources import Resource
from .menu_items import MenuItem


class RecipeBase(BaseModel):
    amount: int


class RecipeCreate(RecipeBase):
    menu_items_id: int
    resource_id: int

class RecipeUpdate(BaseModel):
    menu_items_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    menu_items: "MenuItem" = None
    resource: Resource = None

    class ConfigDict:
        from_attributes = True

# Resolve forward references
from .menu_items import MenuItem
Recipe.update_forward_refs()