from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.controllers.police_occurrence_controller import PoliceOccurrenceController
from src.api.schemas.police_occurrence import PoliceOccurrenceOut
from src.api.schemas.police_occurrence_params import PoliceOccurrenceParams
from src.config.database import get_db

police_occurrence_router = APIRouter(prefix="/police_occurrences", tags=["police_occurrences"])


@police_occurrence_router.get("/", response_model=List[PoliceOccurrenceOut])
def list_police_occurrences(    
    params: PoliceOccurrenceParams = Depends(),
    db: Session = Depends(get_db)
):
    controller = PoliceOccurrenceController(db)
    return controller.list(params=params)