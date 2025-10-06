from typing import List, Optional
from sqlalchemy.orm import Session
from src.api.logic.traffic_logic import TrafficLogic


class TrafficController:
    def __init__(self, db: Session):
        self.logic = TrafficLogic(db)

    def list(self, params) -> List[any]:
        data = self.logic.list(params)
        return data

    def get_by_id(self, traffic_id: int) -> Optional[any]:
        return self.logic.get_by_id(traffic_id)

    def create(self, data) -> any:
        return self.logic.create(data)
