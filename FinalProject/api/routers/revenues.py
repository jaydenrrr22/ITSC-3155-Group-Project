from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..controllers.revenues import get_total_revenues
from ..dependencies.database import get_db
from ..schemas.revenues import DailyRevenue

router = APIRouter(
    tags=['Revenues'],
    prefix="/revenues"
)

@router.get("/", response_model=DailyRevenue)
def total_revenue(date: str = Query(..., description = "Date in YYYY-MM-DD"), db:Session = Depends(get_db)):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date")

    total = get_total_revenues(db, target_date)
    return DailyRevenue(date=str(target_date), total_revenue=total)