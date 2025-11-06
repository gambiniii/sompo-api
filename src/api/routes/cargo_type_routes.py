from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.controllers.cargo_type_controller import CargoTypeController
from src.api.schemas.cargo_type_schemas import CargoTypeOut, CargoTypeParams, CargoTypeCreate, CargoTypeUpdate
from src.config.database import get_db

cargo_type_router = APIRouter(prefix="/cargo_types", tags=["cargo_types"])


@cargo_type_router.get("/", response_model=List[CargoTypeOut])
def list_cargo_types(
    params: CargoTypeParams = Depends(),
    db: Session = Depends(get_db)
):
    controller = CargoTypeController(db)
    return controller.list(params=params)


@cargo_type_router.get("/{type_id}", response_model=CargoTypeOut)
def get_cargo_type(
    type_id: int,
    db: Session = Depends(get_db)
):
    controller = CargoTypeController(db)
    cargo_type = controller.get_by_id(type_id)
    if not cargo_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de carga não encontrado")
    return cargo_type


@cargo_type_router.post("/", response_model=CargoTypeOut, status_code=status.HTTP_201_CREATED)
def create_cargo_type(
    data: CargoTypeCreate,
    db: Session = Depends(get_db)
):
    controller = CargoTypeController(db)
    return controller.create(data)


@cargo_type_router.put("/{type_id}", response_model=CargoTypeOut)
def update_cargo_type(
    type_id: int,
    data: CargoTypeUpdate,
    db: Session = Depends(get_db)
):
    controller = CargoTypeController(db)
    cargo_type = controller.get_by_id(type_id)
    if not cargo_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de carga não encontrado")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cargo_type, key, value)

    db.commit()
    db.refresh(cargo_type)
    return cargo_type


@cargo_type_router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cargo_type(
    type_id: int,
    db: Session = Depends(get_db)
):
    controller = CargoTypeController(db)
    cargo_type = controller.get_by_id(type_id)
    if not cargo_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de carga não encontrado")

    db.delete(cargo_type)
    db.commit()
    return None
