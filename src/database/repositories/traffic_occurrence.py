from sqlalchemy.orm import Session
from database.models import TrafficOccurrence
from base import BaseRepository


class TrafficOccurrenceRepository(BaseRepository[TrafficOccurrence]):
    def __init__(self, db: Session):
        super().__init__(db, TrafficOccurrence)

    # métodos específicos além do CRUD
    def get_by_hexagon(self, h3_id: str):
        return (
            self.db.query(TrafficOccurrence)
            .filter(TrafficOccurrence.h3_id == h3_id)
            .all()
        )

    def get_by_type(self, type_id: int):
        return (
            self.db.query(TrafficOccurrence)
            .filter(TrafficOccurrence.traffic_occurrence_type_id == type_id)
            .all()
        )
