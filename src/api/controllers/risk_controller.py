from src.api.logic.risk_logic import RiskUseCase
from typing import List, Tuple
from datetime import datetime, time

class RiskController:
    def __init__(self):
        self.use_case = RiskUseCase()

    def route_risk_assessment(self, route: List[Tuple[float, float]], expected_hour: int, weekday: int, cargo_type: str = "Cargas Fracionadas"):
        # Converter expected_hour e weekday para datetime
        base_date = datetime(2025, 1, 6)  # Uma segunda-feira
        departure_datetime = datetime.combine(
            base_date.date(),
            time(hour=expected_hour, minute=0, second=0)
        )
        departure_datetime = departure_datetime.replace(day=6 + weekday)

        return self.use_case.predict_route_risk(
            route_coords=route,
            departure_datetime=departure_datetime,
            cargo_type=cargo_type
        )