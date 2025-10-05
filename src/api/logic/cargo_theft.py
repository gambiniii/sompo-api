from sqlalchemy.orm import Session
from typing import Optional
from src.database.repositories.cargo_theft import CargoTheftRepository

class CargoTheftLogic:
    def __init__(self, db: Session):
        self.repo = CargoTheftRepository(db)

    def list(
        self,
        state: Optional[str] = None,
        city: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        offset: int = 0,
        limit: int = 100
    ):
        return self.repo.list(state, city, start_date, end_date, offset, limit)
