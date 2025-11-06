from src.api.logic.accident_risk_logic import AccidentRiskUseCase
from typing import List, Tuple, Optional
from datetime import datetime, time

class AccidentRiskController:
    def __init__(self):
        self.use_case = AccidentRiskUseCase()

    def route_risk_assessment(
        self,
        route: List[Tuple[float, float]],
        expected_hour: int,
        weekday: int,
        cargo_type: str,
        weather_condition: Optional[str] = None
    ):
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
            cargo_type=cargo_type,
            weather_condition=weather_condition
        )
