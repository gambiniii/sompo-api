from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.controllers.cargo_type_controller import CargoTypeController
from src.api.schemas.cargo_type_schemas import CargoTypeOut, CargoTypeParams
from src.config.database import get_db

cargo_type_router = APIRouter(prefix="/cargo_types", tags=["cargo_types"])


@cargo_type_router.get("/", response_model=List[CargoTypeOut])
def list_cargo_types(
    params: CargoTypeParams = Depends(),
    db: Session = Depends(get_db)
):
    controller = CargoTypeController(db)
    return controller.list(params=params)
