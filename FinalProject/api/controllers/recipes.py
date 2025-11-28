from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import recipes as model
from ..schemas.recipes import RecipeCreate, RecipeUpdate


def create(db: Session, request: RecipeCreate):
    new_recipe = model.Recipe(
        menu_item_id=request.menu_item_id,
        resource_id=request.resource_id,
        amount=request.amount
    )

    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_recipe


def read_all(db: Session):
    try:
        return db.query(model.Recipe).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, recipe_id: int):
    try:
        recipe = (
            db.query(model.Recipe)
            .filter(model.Recipe.id == recipe_id)
            .first()
        )
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe ID not found"
            )
        return recipe

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def update(db: Session, recipe_id: int, request: RecipeUpdate):
    try:
        recipe_query = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        recipe_db = recipe_query.first()

        if not recipe_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe ID not found"
            )

        update_data = request.dict(exclude_unset=True)
        recipe_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(recipe_db)
        return recipe_db

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def delete(db: Session, recipe_id: int):
    try:
        recipe_query = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        recipe_db = recipe_query.first()

        if not recipe_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe ID not found"
            )

        recipe_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Recipe deleted successfully"}

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)