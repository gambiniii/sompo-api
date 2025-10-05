from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.repositories.traffic_occurrence_repository import TrafficOccurrenceRepository

class TrafficOccurrenceLogic:
    def __init__(self, db: Session):
        self.repository = TrafficOccurrenceRepository(db)

    def list(self, params) -> List[any]:
        return self.repository.list(params)

    def get_by_id(self, occurrence_id: int) -> Optional[any]:
        return self.repository.get_by_id(occurrence_id)

    def create(self, data) -> any:
        return self.repository.create(data)