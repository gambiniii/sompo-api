from typing import List
from sqlalchemy.orm import Session
from src.database.entities.cargo_type import CargoType
from src.database.repositories.base import BaseRepository


class CargoTypeRepository(BaseRepository[CargoType]):
    def __init__(self, db: Session):
        super().__init__(db, CargoType)

    def list(self, params) -> List[CargoType]:
        query = self.db.query(CargoType)

        if params.name:
            query = query.filter(CargoType.name.ilike(f"%{params.name}%"))
        if params.min_theft:
            query = query.filter(CargoType.theft >= params.min_theft)
        if params.max_theft:
            query = query.filter(CargoType.theft <= params.max_theft)
        if params.min_accident:
            query = query.filter(CargoType.accident >= params.min_accident)
        if params.max_accident:
            query = query.filter(CargoType.accident <= params.max_accident)
        if params.min_global_risk_level:
            query = query.filter(CargoType.global_risk_level >= params.min_global_risk_level)
        if params.max_global_risk_level:
            query = query.filter(CargoType.global_risk_level <= params.max_global_risk_level)

        return query.offset(params.offset).limit(params.limit).all()
