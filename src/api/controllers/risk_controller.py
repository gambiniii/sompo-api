from api.logic.risk_logic import RiskUseCase
from typing import List, Tuple

class RiskController:
    def __init__(self):
        self.use_case = RiskUseCase()

    def route_risk_assessment(self, route: List[Tuple[float, float]], expected_hour: int, weekday: int):
        return self.use_case.route_risk_assessment(route, expected_hour, weekday)