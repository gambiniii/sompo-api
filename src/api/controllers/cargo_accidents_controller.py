from typing import List, Optional
from sqlalchemy.orm import Session
from src.api.logic.cargo_accidents_logic import CargoAccidentsLogic


class CargoAccidentsController:
    def __init__(self, db: Session):
        self.logic = CargoAccidentsLogic(db)

    def list(self, params) -> List[any]:
        data = self.logic.list(params)
        return data

    def get_by_id(self, accident_id: int) -> Optional[any]:
        return self.logic.get_by_id(accident_id)

    def create(self, data) -> any:
        return self.logic.create(data)
