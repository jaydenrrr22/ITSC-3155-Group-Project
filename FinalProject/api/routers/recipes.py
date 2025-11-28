from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import recipes as controller
from ..schemas.recipes import Recipe, RecipeCreate, RecipeUpdate
from ..dependencies.database import get_db


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)


@router.post("/", response_model=Recipe)
def create_recipe(request: RecipeCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)


@router.get("/", response_model=list[Recipe])
def get_all_recipes(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, recipe_id)


@router.put("/{recipe_id}", response_model=Recipe)
def update_recipe(
    recipe_id: int,
    request: RecipeUpdate,
    db: Session = Depends(get_db)
):
    return controller.update(db, recipe_id, request)


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, recipe_id)