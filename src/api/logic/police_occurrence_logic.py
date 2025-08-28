from typing import List
from src.database.repositories.police_occurrence_repository import PoliceOccurrenceRepository
from src.database.entities.police_occurrence import PoliceOccurrence

class PoliceOccurrenceLogic:
        def __init__(self):
            self.repository = PoliceOccurrenceRepository()

        def list(self, params) -> List[PoliceOccurrence]:
            return self.repository.list(params)

