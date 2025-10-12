from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
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

    def get_heatmap_data(self, limit: int = 10000) -> List[CargoTheft]:
        """
        Retorna apenas as coordenadas para heatmap.
        Otimizado para performance com limite de registros.
        """
        return (
            self.db.query(CargoTheft)
            .order_by(CargoTheft.occurred_at.desc())
            .limit(limit)
            .all()
        )
    
    def get_monthly_summary(self):
        """
        Retorna contagem de roubos por mês, para tabela/gráfico.
        """
        results = (
            self.db.query(
                func.date_trunc('month', CargoTheft.occurred_at).label('month'),
                func.count(CargoTheft.id).label('count')
            )
            .group_by('month')
            .order_by('month')
            .all()
        )

        return [{"month": r.month.strftime("%Y-%m"), "count": r.count} for r in results]

