from sqlalchemy.orm import Session
from database.entities.traffice_occurrence import PoliceOccurrence
from base import BaseRepository


class TrafficOccurrenceRepository(BaseRepository[PoliceOccurrence]):
    def __init__(self, db: Session):
        super().__init__(db, PoliceOccurrence)

    # métodos específicos além do CRUD
    def get_by_hexagon(self, h3_id: str):
        return (
            self.db.query(PoliceOccurrence)
            .filter(PoliceOccurrence.h3_id == h3_id)
            .all()
        )

    def get_by_type(self, type_id: int):
        return (
            self.db.query(PoliceOccurrence)
            .filter(PoliceOccurrence.traffic_occurrence_type_id == type_id)
            .all()
        )
