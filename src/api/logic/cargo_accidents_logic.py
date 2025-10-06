from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.repositories.cargo_accidents_repository import CargoAccidentsRepository


class CargoAccidentsLogic:
    def __init__(self, db: Session):
        self.repository = CargoAccidentsRepository(db)

    def list(self, params) -> List[any]:
        return self.repository.list(params)

    def get_by_id(self, accident_id: int) -> Optional[any]:
        return self.repository.get(accident_id)

    def create(self, data) -> any:
        return self.repository.create(data)
