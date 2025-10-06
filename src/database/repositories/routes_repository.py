from typing import List
from sqlalchemy.orm import Session
from src.database.entities.routes import Routes
from src.database.repositories.base import BaseRepository


class RoutesRepository(BaseRepository[Routes]):
    def __init__(self, db: Session):
        super().__init__(db, Routes)

    def list(self, params) -> List[Routes]:
        query = self.db.query(Routes)

        if params.route:
            query = query.filter(Routes.route.ilike(f"%{params.route}%"))
        if params.highway:
            query = query.filter(Routes.highway.ilike(f"%{params.highway}%"))
        if params.min_total_traffic:
            query = query.filter(Routes.total_traffic >= params.min_total_traffic)
        if params.max_total_traffic:
            query = query.filter(Routes.total_traffic <= params.max_total_traffic)

        return query.offset(params.offset).limit(params.limit).all()
