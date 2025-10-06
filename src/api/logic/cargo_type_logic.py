from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.repositories.cargo_type_repository import CargoTypeRepository


class CargoTypeLogic:
    def __init__(self, db: Session):
        self.repository = CargoTypeRepository(db)

    def list(self, params) -> List[any]:
        return self.repository.list(params)

    def get_by_id(self, type_id: int) -> Optional[any]:
        return self.repository.get(type_id)

    def create(self, data) -> any:
        return self.repository.create(data)
