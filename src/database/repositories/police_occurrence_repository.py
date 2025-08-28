from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session

from database.entities.police_occurrence import PoliceOccurrence
from base import BaseRepository
from src.api.schemas.police_occurrence import PoliceOccurrenceOut
from src.api.schemas.police_occurrence_params import PoliceOccurrenceParams


class PoliceOccurrenceRepository(BaseRepository[PoliceOccurrence]):
    def __init__(self, db: Session):
        super().__init__(db, PoliceOccurrence)

    def list(self, params: PoliceOccurrenceParams) -> List[PoliceOccurrenceOut]:
        q = self.db.query(PoliceOccurrence)
        conds = []

        if params.type_id is not None:
            conds.append(PoliceOccurrence.police_occurrence_type_id == params.type_id)
        
        if params.h3_id is not None:
            conds.append(PoliceOccurrence.h3_id == params.h3_id)
        
        if params.start_date is not None:
            conds.append(PoliceOccurrence.occurred_at >= params.start_date)
        
        if params.end_date is not None:
            conds.append(PoliceOccurrence.occurred_at <= params.end_date)
        
        if params.min_lat is not None:
            conds.append(PoliceOccurrence.lat >= params.min_lat)
        
        if params.max_lat is not None:
            conds.append(PoliceOccurrence.lat <= params.max_lat)
        
        if params.min_lng is not None:
            conds.append(PoliceOccurrence.lng >= params.min_lng)
        
        if params.max_lng is not None:
            conds.append(PoliceOccurrence.lng <= params.max_lng)

        if params.conds:
            q = q.filter(and_(*conds))

        return q.offset(params.offset).limit(min(1000, max(1, params.limit))).all()