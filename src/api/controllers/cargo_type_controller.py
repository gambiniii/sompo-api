from typing import List, Optional
from sqlalchemy.orm import Session
from src.api.logic.cargo_type_logic import CargoTypeLogic


class CargoTypeController:
    def __init__(self, db: Session):
        self.logic = CargoTypeLogic(db)

    def list(self, params) -> List[any]:
        data = self.logic.list(params)
        return data

    def get_by_id(self, type_id: int) -> Optional[any]:
        return self.logic.get_by_id(type_id)

    def create(self, data) -> any:
        return self.logic.create(data)
