from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from src.database.entities.police_occurrence_type import TrafficOccurrenceType
from src.api.schemas.police_occurrence_type import (
    TrafficOccurrenceTypeCreate,
    TrafficOccurrenceTypeOut,
)

class TrafficOccurrenceTypeController:
    def create(self, db: Session, data: TrafficOccurrenceTypeCreate) -> TrafficOccurrenceTypeOut:
        exists = (
            db.query(TrafficOccurrenceType)
              .filter(func.lower(TrafficOccurrenceType.name) == data.name.strip().lower())
              .first()
        )
        if exists:
            raise ValueError("police_occurrence_type with this name already exists")

        obj = TrafficOccurrenceType(
            name=data.name.strip(),
            description=(data.description or None),
        )
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            
            raise ValueError("police_occurrence_type name must be unique")
        db.refresh(obj)
        return obj

    def get_by_id(self, db: Session, type_id: int) -> Optional[TrafficOccurrenceTypeOut]:
        return db.query(TrafficOccurrenceType).filter(TrafficOccurrenceType.id == type_id).first()

    def list(self, db: Session, *, q: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[TrafficOccurrenceTypeOut]:
        query = db.query(TrafficOccurrenceType)
        if q:
            like = f"%{q.strip().lower()}%"
            query = query.filter(func.lower(TrafficOccurrenceType.name).like(like))
        return query.order_by(TrafficOccurrenceType.id.asc()).offset(offset).limit(min(1000, max(1, limit))).all()
