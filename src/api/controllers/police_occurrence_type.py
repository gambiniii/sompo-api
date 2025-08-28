from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from src.database.entities.police_occurrence_type import PoliceOccurrenceType
from src.api.schemas.police_occurrence_type import (
    PoliceOccurrenceTypeCreate,
    PoliceOccurrenceTypeOut,
)

class PoliceOccurrenceTypeController:
    def create(self, db: Session, data: PoliceOccurrenceTypeCreate) -> PoliceOccurrenceTypeOut:
        # opcional: normalizar para evitar duplicados por case/espaço
        exists = (
            db.query(PoliceOccurrenceType)
              .filter(func.lower(PoliceOccurrenceType.name) == data.name.strip().lower())
              .first()
        )
        if exists:
            raise ValueError("police_occurrence_type with this name already exists")

        obj = PoliceOccurrenceType(
            name=data.name.strip(),
            description=(data.description or None),
        )
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # cobre UNIQUE no banco, caso exista
            raise ValueError("police_occurrence_type name must be unique")
        db.refresh(obj)
        return obj

    def get_by_id(self, db: Session, type_id: int) -> Optional[PoliceOccurrenceTypeOut]:
        return db.query(PoliceOccurrenceType).filter(PoliceOccurrenceType.id == type_id).first()

    def list(self, db: Session, *, q: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[PoliceOccurrenceTypeOut]:
        query = db.query(PoliceOccurrenceType)
        if q:
            like = f"%{q.strip().lower()}%"
            query = query.filter(func.lower(PoliceOccurrenceType.name).like(like))
        return query.order_by(PoliceOccurrenceType.id.asc()).offset(offset).limit(min(1000, max(1, limit))).all()
