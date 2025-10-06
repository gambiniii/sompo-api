from typing import List
from sqlalchemy.orm import Session
from src.database.entities.traffic import Traffic
from src.database.repositories.base import BaseRepository


class TrafficRepository(BaseRepository[Traffic]):
    def __init__(self, db: Session):
        super().__init__(db, Traffic)

    def list(self, params) -> List[Traffic]:
        query = self.db.query(Traffic)

        if params.direction:
            query = query.filter(Traffic.direction == params.direction)
        if params.uf:
            query = query.filter(Traffic.uf == params.uf)
        if params.highway:
            query = query.filter(Traffic.highway == params.highway)
        if params.route_id:
            query = query.filter(Traffic.route_id == params.route_id)
        if params.start_date:
            query = query.filter(Traffic.date >= params.start_date)
        if params.end_date:
            query = query.filter(Traffic.date <= params.end_date)
        if params.min_lat:
            query = query.filter(Traffic.latitude >= params.min_lat)
        if params.max_lat:
            query = query.filter(Traffic.latitude <= params.max_lat)
        if params.min_lng:
            query = query.filter(Traffic.longitude >= params.min_lng)
        if params.max_lng:
            query = query.filter(Traffic.longitude <= params.max_lng)

        return query.offset(params.offset).limit(params.limit).all()
