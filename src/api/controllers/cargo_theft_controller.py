from typing import List, Optional
from sqlalchemy.orm import Session
from src.api.logic.cargo_theft_logic import CargoTheftLogic


class CargoTheftController:
    def __init__(self, db: Session):
        self.logic = CargoTheftLogic(db)

    def list(self, params) -> List[any]:
        data = self.logic.list(params)
        return data

    def get_by_id(self, theft_id: int) -> Optional[any]:
        return self.logic.get_by_id(theft_id)

    def create(self, data) -> any:
        return self.logic.create(data)
