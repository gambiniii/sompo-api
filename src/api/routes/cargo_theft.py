from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from src.api.controllers.cargo_theft import CargoTheftController
from src.database.session import get_db

router = APIRouter(prefix="/cargo_theft", tags=["Cargo Theft"])

@router.get("/")
def list_cargo_theft(
    state: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    offset: int = Query(0),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    controller = CargoTheftController(db)
    return controller.list(
        state=state,
        city=city,
        start_date=start_date,
        end_date=end_date,
        offset=offset,
        limit=limit
    )
