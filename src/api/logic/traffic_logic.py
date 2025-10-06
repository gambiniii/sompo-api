from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.repositories.traffic_repository import TrafficRepository


class TrafficLogic:
    def __init__(self, db: Session):
        self.repository = TrafficRepository(db)

    def list(self, params) -> List[any]:
        return self.repository.list(params)

    def get_by_id(self, traffic_id: int) -> Optional[any]:
        return self.repository.get(traffic_id)

    def create(self, data) -> any:
        return self.repository.create(data)
