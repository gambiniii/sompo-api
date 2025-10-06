from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.repositories.cargo_theft_repository import CargoTheftRepository


class CargoTheftLogic:
    def __init__(self, db: Session):
        self.repository = CargoTheftRepository(db)

    def list(self, params) -> List[any]:
        return self.repository.list(params)

    def get_by_id(self, theft_id: int) -> Optional[any]:
        return self.repository.get(theft_id)

    def create(self, data) -> any:
        return self.repository.create(data)
