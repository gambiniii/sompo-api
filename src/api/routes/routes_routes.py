from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.controllers.routes_controller import RoutesController
from src.api.schemas.routes_schemas import RoutesOut, RoutesParams
from src.config.database import get_db

routes_router = APIRouter(prefix="/routes", tags=["routes"])


@routes_router.get("/", response_model=List[RoutesOut])
def list_routes(
    params: RoutesParams = Depends(),
    db: Session = Depends(get_db)
):
    controller = RoutesController(db)
    return controller.list(params=params)
