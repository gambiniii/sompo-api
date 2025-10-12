from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict

from src.api.controllers.cargo_accidents_controller import CargoAccidentsController
from src.api.schemas.cargo_accidents_schemas import (
    CargoAccidentsOut,
    CargoAccidentsParams,
)
from src.config.database import get_db

cargo_accidents_router = APIRouter(prefix="/cargo_accidents", tags=["cargo_accidents"])


@cargo_accidents_router.get("/", response_model=List[CargoAccidentsOut])
def list_cargo_accidents(
    params: CargoAccidentsParams = Depends(), db: Session = Depends(get_db)
):
    controller = CargoAccidentsController(db)
    return controller.list(params=params)


@cargo_accidents_router.get("/heatmap")
def get_cargo_accidents_heatmap(limit: int = 10000, db: Session = Depends(get_db)):
    """
    Retorna dados de acidentes de carga para exibição em heatmap.
    Retorna apenas coordenadas (latitude, longitude) e intensidade.
    """
    controller = CargoAccidentsController(db)
    return controller.get_heatmap_data(limit=limit)


@cargo_accidents_router.get("/monthly_summary", response_model=List[Dict])
def monthly_summary(limit: int = 10000, db: Session = Depends(get_db)):
    controller = CargoAccidentsController(db)
    return controller.get_monthly_summary(limit=limit)
