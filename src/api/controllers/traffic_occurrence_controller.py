from typing import List, Optional
from sqlalchemy.orm import Session
from src.api.logic.traffic_occurrence_logic import TrafficOccurrenceLogic

class TrafficOccurrenceController:
    def __init__(self, db: Session):
        self.logic = TrafficOccurrenceLogic(db)

    def list(self, params) -> List[any]:
        data = self.logic.list(params)
        return data

    def get_by_id(self, occurrence_id: int) -> Optional[any]:
        return self.logic.get_by_id(occurrence_id)

    def create(self, data) -> any:
        return self.logic.create(data)
