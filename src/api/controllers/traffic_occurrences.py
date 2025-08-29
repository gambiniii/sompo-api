from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.entities.traffice_occurrence import TrafficOccurrence
from src.database.entities.traffic_occurrence_type import TrafficOccurrenceType
from src.api.schemas.police_occurrence import (
    TrafficOccurrenceCreate, TrafficOccurrenceOut
)

class TrafficOccurrenceController:
    def create(self, db: Session, data: TrafficOccurrenceCreate):
        exists = (
            db.query(TrafficOccurrenceType.id)
            .filter(TrafficOccurrenceType.id == int(data.police_occurrence_type_id))
            .first()
        )
        if not exists:
            raise ValueError("invalid traffic_occurrence_type_id")

        obj = TrafficOccurrence(
            police_occurrence_type_id=int(data.police_occurrence_type_id),
            description=data.description,
            lat=float(data.lat),
            lng=float(data.lng),
            occurred_at=data.occurred_at,
            h3_id=data.h3_id,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj


    def get_by_id(self, db: Session, occurrence_id: int) -> Optional[TrafficOccurrenceOut]:
        return db.query(TrafficOccurrence).filter(TrafficOccurrence.id == occurrence_id).first()

    def list(
        self, db: Session,
        *, type_id: Optional[int] = None,
        start_date: Optional[date] = None, end_date: Optional[date] = None,
        h3_id: Optional[str] = None,
        min_lat: Optional[float] = None, max_lat: Optional[float] = None,
        min_lng: Optional[float] = None, max_lng: Optional[float] = None,
        limit: int = 100, offset: int = 0,
    ) -> List[TrafficOccurrenceOut]:
        q = db.query(TrafficOccurrence)
        conds = []
        if type_id is not None: conds.append(TrafficOccurrence.police_occurrence_type_id == type_id)
        if h3_id is not None:   conds.append(TrafficOccurrence.h3_id == h3_id)
        if start_date is not None: conds.append(TrafficOccurrence.occurred_at >= start_date)
        if end_date is not None:   conds.append(TrafficOccurrence.occurred_at <= end_date)
        if min_lat is not None: conds.append(TrafficOccurrence.lat >= min_lat)
        if max_lat is not None: conds.append(TrafficOccurrence.lat <= max_lat)
        if min_lng is not None: conds.append(TrafficOccurrence.lng >= min_lng)
        if max_lng is not None: conds.append(TrafficOccurrence.lng <= max_lng)
        if conds: q = q.filter(and_(*conds))
        return q.offset(offset).limit(min(1000, max(1, limit))).all()
