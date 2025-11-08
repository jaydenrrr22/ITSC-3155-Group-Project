from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import customers as controller
from ..schemas import customers as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Customers'],
    prefix="/customers"
)

@router.post("/", response_model=schema.customers)
def create(request: schema.customersCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)