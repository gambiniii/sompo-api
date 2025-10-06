from typing import List
from sqlalchemy.orm import Session
from src.database.entities.cargo_accidents import CargoAccidents
from src.database.repositories.base import BaseRepository


class CargoAccidentsRepository(BaseRepository[CargoAccidents]):
    def __init__(self, db: Session):
        super().__init__(db, CargoAccidents)

    def list(self, params) -> List[CargoAccidents]:
        query = self.db.query(CargoAccidents)

        if params.state:
            query = query.filter(CargoAccidents.state == params.state)
        if params.city:
            query = query.filter(CargoAccidents.city == params.city)
        if params.highway:
            query = query.filter(CargoAccidents.highway == params.highway)
        if params.start_date:
            query = query.filter(CargoAccidents.date >= params.start_date)
        if params.end_date:
            query = query.filter(CargoAccidents.date <= params.end_date)
        if params.accident_type:
            query = query.filter(CargoAccidents.accident_type == params.accident_type)
        if params.min_lat:
            query = query.filter(CargoAccidents.latitude >= params.min_lat)
        if params.max_lat:
            query = query.filter(CargoAccidents.latitude <= params.max_lat)
        if params.min_lng:
            query = query.filter(CargoAccidents.longitude >= params.min_lng)
        if params.max_lng:
            query = query.filter(CargoAccidents.longitude <= params.max_lng)

        return query.offset(params.offset).limit(params.limit).all()
