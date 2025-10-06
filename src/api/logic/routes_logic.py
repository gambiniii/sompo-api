from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.repositories.routes_repository import RoutesRepository


class RoutesLogic:
    def __init__(self, db: Session):
        self.repository = RoutesRepository(db)

    def list(self, params) -> List[any]:
        return self.repository.list(params)

    def get_by_id(self, route_id: int) -> Optional[any]:
        return self.repository.get(route_id)

    def create(self, data) -> any:
        return self.repository.create(data)
