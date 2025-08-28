from typing import List, Optional
from src.api.logic.police_occurrence_logic import PoliceOccurrenceLogic

class PoliceOccurrenceController:
    def __init__(self):
        self.logic = PoliceOccurrenceLogic()

    def list(self, params) -> List[any]:
        data = self.logic.list(params)
        return data
    
    def get_by_id(self, occurrence_id: int) -> Optional[any]:
        # return db.query(PoliceOccurrence).filter(PoliceOccurrence.id == occurrence_id).first()
        return
