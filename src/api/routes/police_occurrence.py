from typing import List
from fastapi import APIRouter, Depends

from src.api.controllers.police_occurrence import PoliceOccurrenceController
from src.api.schemas.police_occurrence import PoliceOccurrenceOut
from src.api.schemas.police_occurrence_params import PoliceOccurrenceParams

police_occurrence_router = APIRouter(prefix="/police_occurrences", tags=["police_occurrences"])
controller = PoliceOccurrenceController()

@police_occurrence_router.get("/", response_model=List[PoliceOccurrenceOut])
def list_police_occurrences(params: PoliceOccurrenceParams = Depends()):
    return controller.list(params=params)