from typing import List, Optional
from sqlalchemy.orm import Session
from src.api.logic.routes_logic import RoutesLogic


class RoutesController:
    def __init__(self, db: Session):
        self.logic = RoutesLogic(db)

    def list(self, params) -> List[any]:
        data = self.logic.list(params)
        return data

    def get_by_id(self, route_id: int) -> Optional[any]:
        return self.logic.get_by_id(route_id)

    def create(self, data) -> any:
        return self.logic.create(data)
