from typing import List
from sqlalchemy.orm import Session
from src.database.repositories.police_occurrence_repository import PoliceOccurrenceRepository

class PoliceOccurrenceLogic:
    def __init__(self, db: Session):
        self.repository = PoliceOccurrenceRepository(db)

    def list(self, params) -> List[any]:
        return self.repository.list(params)

