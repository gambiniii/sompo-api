from typing import List, Optional
from sqlalchemy.orm import Session
from src.api.logic.cargo_accidents_logic import CargoAccidentsLogic


class CargoAccidentsController:
    def __init__(self, db: Session):
        self.logic = CargoAccidentsLogic(db)

    def list(self, params) -> List[any]:
        data = self.logic.list(params)

        for acc in data:
            acc.latitude = round(acc.latitude, 6)
            acc.longitude = round(acc.longitude, 6)

        return data

    def get_by_id(self, accident_id: int) -> Optional[any]:
        return self.logic.get_by_id(accident_id)

    def create(self, data) -> any:
        return self.logic.create(data)

    def get_heatmap_data(self, limit: int = 10000):
        """Retorna dados para heatmap de acidentes"""
        return self.logic.get_heatmap_data(limit=limit)

    def get_monthly_summary(self, limit: int = 10000):
        return self.logic.get_monthly_summary(limit=limit)
