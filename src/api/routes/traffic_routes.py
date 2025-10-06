from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.controllers.traffic_controller import TrafficController
from src.api.schemas.traffic_schemas import TrafficOut, TrafficParams
from src.config.database import get_db

traffic_router = APIRouter(prefix="/traffic", tags=["traffic"])


@traffic_router.get("/", response_model=List[TrafficOut])
def list_traffic(
    params: TrafficParams = Depends(),
    db: Session = Depends(get_db)
):
    controller = TrafficController(db)
    return controller.list(params=params)
