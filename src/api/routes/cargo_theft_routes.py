from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.controllers.cargo_theft_controller import CargoTheftController
from src.api.schemas.cargo_theft_schemas import CargoTheftOut, CargoTheftParams
from src.config.database import get_db

cargo_theft_router = APIRouter(prefix="/cargo_thefts", tags=["cargo_thefts"])


@cargo_theft_router.get("/", response_model=List[CargoTheftOut])
def list_cargo_thefts(
    params: CargoTheftParams = Depends(),
    db: Session = Depends(get_db)
):
    controller = CargoTheftController(db)
    return controller.list(params=params)
