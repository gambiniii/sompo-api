from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.api.controllers.police_occurrence import PoliceOccurrenceController
from src.api.schemas.police_occurrence import TrafficOccurrenceCreate, TrafficOccurrenceOut

police_occurrence_router = APIRouter(prefix="/police_occurrences", tags=["police_occurrences"])
controller = PoliceOccurrenceController()

@police_occurrence_router.get("/", response_model=List[TrafficOccurrenceOut])
def list_occurrences(
    type_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    h3_id: Optional[str] = Query(None),
    min_lat: Optional[float] = Query(None), max_lat: Optional[float] = Query(None),
    min_lng: Optional[float] = Query(None), max_lng: Optional[float] = Query(None),
    limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return controller.list(
        db, type_id=type_id, start_date=start_date, end_date=end_date, h3_id=h3_id,
        min_lat=min_lat, max_lat=max_lat, min_lng=min_lng, max_lng=max_lng,
        limit=limit, offset=offset
    )

@police_occurrence_router.get("/{occurrence_id}", response_model=TrafficOccurrenceOut)
def get_occurrence(occurrence_id: int, db: Session = Depends(get_db)):
    obj = controller.get_by_id(db, occurrence_id)
    if not obj:
        raise HTTPException(status_code=404, detail="police_occurrence not found")
    return obj

@police_occurrence_router.post("/", response_model=TrafficOccurrenceOut, status_code=201)
def create_occurrence(payload: TrafficOccurrenceCreate, db: Session = Depends(get_db)):
    try:
        return controller.create(db, payload)
    except ValueError as e:  # <- FK inválida, etc.
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="internal error")
