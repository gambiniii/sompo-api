from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.controllers.cargo_accidents_controller import CargoAccidentsController
from src.api.schemas.cargo_accidents_schemas import CargoAccidentsOut, CargoAccidentsParams
from src.config.database import get_db

cargo_accidents_router = APIRouter(prefix="/cargo_accidents", tags=["cargo_accidents"])


@cargo_accidents_router.get("/", response_model=List[CargoAccidentsOut])
def list_cargo_accidents(
    params: CargoAccidentsParams = Depends(),
    db: Session = Depends(get_db)
):
    controller = CargoAccidentsController(db)
    return controller.list(params=params)
