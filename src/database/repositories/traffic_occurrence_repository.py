from typing import List
from sqlalchemy.orm import Session
from src.database.entities.traffic_occurrence import TrafficOccurrence
from src.database.repositories.base import BaseRepository

class TrafficOccurrenceRepository(BaseRepository[TrafficOccurrence]):
    def __init__(self, db: Session):
        super().__init__(db, TrafficOccurrence)

    def list(self, params) -> List[any]:
        query = self.db.query(TrafficOccurrence)

        if params.type_id:
            query = query.filter(TrafficOccurrence.traffic_occurrence_type_id == params.type_id)
        if params.h3_id:
            query = query.filter(TrafficOccurrence.h3_id == params.h3_id)
        if params.start_date:
            query = query.filter(TrafficOccurrence.occurred_at >= params.start_date)
        if params.end_date:
            query = query.filter(TrafficOccurrence.occurred_at <= params.end_date)
        if params.min_lat:
            query = query.filter(TrafficOccurrence.lat >= params.min_lat)
        if params.max_lat:
            query = query.filter(TrafficOccurrence.lat <= params.max_lat)
        if params.min_lng:
            query = query.filter(TrafficOccurrence.lng >= params.min_lng)
        if params.max_lng:
            query = query.filter(TrafficOccurrence.lng <= params.max_lng)

        return query.offset(params.offset).limit(params.limit).all()

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
