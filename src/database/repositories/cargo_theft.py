from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional

class CargoTheftRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        state: Optional[str] = None,
        city: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        offset: int = 0,
        limit: int = 100
    ):
        from src.database.entities.cargo_theft import CargoTheft  # import local para evitar loop

        q = self.db.query(CargoTheft)
        conds = []

        if state:
            conds.append(CargoTheft.state.ilike(f"%{state}%"))
        if city:
            conds.append(CargoTheft.city.ilike(f"%{city}%"))
        if start_date:
            conds.append(CargoTheft.occurred_at >= start_date)
        if end_date:
            conds.append(CargoTheft.occurred_at <= end_date)

        if conds:
            q = q.filter(and_(*conds))

        q = q.order_by(CargoTheft.occurred_at.desc())

        return q.offset(offset).limit(min(1000, max(1, limit))).all()
