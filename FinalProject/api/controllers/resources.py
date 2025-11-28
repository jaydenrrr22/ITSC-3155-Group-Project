from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import resources as model
from ..schemas.resources import ResourceCreate, ResourceUpdate
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request: ResourceCreate):
    new_resource = model.Resource(
        item = request.item,
        amount = request.amount,
        unit = request.unit
    )
    try:
        db.add(new_resource)
        db.commit()
        db.refresh(new_resource)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_resource

def read_all(db: Session):
    try:
        result = db.query(model.Resource).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id):
    try:
        item = db.query(model.Resource).filter(model.Resource.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, item_id: int, request: ResourceUpdate):
    try:
        db_item = db.query(model.Resource).filter(model.Resource.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return db_item

def delete(db: Session, item_id):
    try:
        item = db.query(model.Resource).filter(model.Resource.id == item_id)
        db_item = item.first()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)