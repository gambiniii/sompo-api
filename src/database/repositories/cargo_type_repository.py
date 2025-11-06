from typing import List
from sqlalchemy.orm import Session
from src.database.entities.cargo_type import CargoType
from src.database.repositories.base import BaseRepository


class CargoTypeRepository(BaseRepository[CargoType]):
    def __init__(self, db: Session):
        super().__init__(db, CargoType)

    def list(self, params) -> List[CargoType]:
        query = self.db.query(CargoType)

        if params.categoria:
            query = query.filter(CargoType.categoria.ilike(f"%{params.categoria}%"))
        if params.descricao:
            query = query.filter(CargoType.descricao.ilike(f"%{params.descricao}%"))
        if params.min_risco_roubo is not None:
            query = query.filter(CargoType.risco_roubo_percentual >= params.min_risco_roubo)
        if params.max_risco_roubo is not None:
            query = query.filter(CargoType.risco_roubo_percentual <= params.max_risco_roubo)
        if params.min_risco_acidente is not None:
            query = query.filter(CargoType.risco_acidente_percentual >= params.min_risco_acidente)
        if params.max_risco_acidente is not None:
            query = query.filter(CargoType.risco_acidente_percentual <= params.max_risco_acidente)
        if params.impacto_ambiental:
            query = query.filter(CargoType.impacto_ambiental.ilike(f"%{params.impacto_ambiental}%"))

        return query.offset(params.offset).limit(params.limit).all()
