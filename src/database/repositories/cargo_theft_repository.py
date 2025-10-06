from typing import List
from sqlalchemy.orm import Session
from src.database.entities.cargo_theft import CargoTheft
from src.database.repositories.base import BaseRepository


class CargoTheftRepository(BaseRepository[CargoTheft]):
    def __init__(self, db: Session):
        super().__init__(db, CargoTheft)

    def list(self, params) -> List[CargoTheft]:
        query = self.db.query(CargoTheft)

        if params.state:
            query = query.filter(CargoTheft.state == params.state)
        if params.city:
            query = query.filter(CargoTheft.city == params.city)
        if params.start_date:
            query = query.filter(CargoTheft.occurred_at >= params.start_date)
        if params.end_date:
            query = query.filter(CargoTheft.occurred_at <= params.end_date)
        if params.min_lat:
            query = query.filter(CargoTheft.lat >= params.min_lat)
        if params.max_lat:
            query = query.filter(CargoTheft.lat <= params.max_lat)
        if params.min_lng:
            query = query.filter(CargoTheft.lng >= params.min_lng)
        if params.max_lng:
            query = query.filter(CargoTheft.lng <= params.max_lng)

        return query.offset(params.offset).limit(params.limit).all()
