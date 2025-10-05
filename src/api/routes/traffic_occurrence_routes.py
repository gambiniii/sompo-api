from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.controllers.traffic_occurrence_controller import TrafficOccurrenceController
from src.api.schemas.traffic_occurrences import TrafficOccurrenceOut
from src.api.schemas.traffic_occurrence_types import TrafficOccurrenceParams
from src.config.database import get_db

traffic_occurrence_router = APIRouter(prefix="/traffic_occurrences", tags=["traffic_occurrences"])


@traffic_occurrence_router.get("/", response_model=List[TrafficOccurrenceOut])
def list_traffic_occurrences(
    params: TrafficOccurrenceParams = Depends(),
    db: Session = Depends(get_db)
):
    controller = TrafficOccurrenceController(db)
    return controller.list(params=params)
