from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.api.controllers.police_occurrence_type import PoliceOccurrenceTypeController
from src.api.schemas.police_occurrence_type import (
    PoliceOccurrenceTypeCreate,
    PoliceOccurrenceTypeOut,
)

police_occurrence_type_router = APIRouter(
    prefix="/police_occurrence_types",
    tags=["police_occurrence_types"],
)

controller = PoliceOccurrenceTypeController()

# GET /police_occurrence_types
@police_occurrence_type_router.get("/", response_model=List[PoliceOccurrenceTypeOut])
def list_types(
    q: Optional[str] = Query(None, description="filtro por nome (contains, case-insensitive)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return controller.list(db, q=q, limit=limit, offset=offset)

# GET /police_occurrence_types/{id}
@police_occurrence_type_router.get("/{type_id}", response_model=PoliceOccurrenceTypeOut)
def get_type(type_id: int, db: Session = Depends(get_db)):
    obj = controller.get_by_id(db, type_id)
    if not obj:
        raise HTTPException(status_code=404, detail="police_occurrence_type not found")
    return obj

# POST /police_occurrence_types
@police_occurrence_type_router.post("/", response_model=PoliceOccurrenceTypeOut, status_code=201)
def create_type(payload: PoliceOccurrenceTypeCreate, db: Session = Depends(get_db)):
    try:
        return controller.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="internal error")
