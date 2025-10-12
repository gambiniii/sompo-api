from typing import List, Optional
from sqlalchemy.orm import Session
from src.api.logic.cargo_theft_logic import CargoTheftLogic


class CargoTheftController:
    def __init__(self, db: Session):
        self.logic = CargoTheftLogic(db)

    def list(self, params) -> List[any]:
        data = self.logic.list(params)

        for acc in data:
            acc.lat = round(acc.lat, 6)
            acc.lng = round(acc.lng, 6)

        return data

    def get_by_id(self, theft_id: int) -> Optional[any]:
        return self.logic.get_by_id(theft_id)

    def create(self, data) -> any:
        return self.logic.create(data)

    def get_heatmap_data(self, limit: int = 10000):
        """Retorna dados para heatmap de roubos"""
        return self.logic.get_heatmap_data(limit=limit)

    def get_monthly_summary(self):
        """Resumo de roubos por mês"""
        return self.logic.get_monthly_summary()
