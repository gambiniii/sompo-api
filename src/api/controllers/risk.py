from src.api.logic.risk import RiskUseCase
from typing import List, Tuple

class RiskController:
    def __init__(self):
        self.use_case = RiskUseCase()

    def route_risk_assessment(self, route: List[Tuple[float, float]]):
        return self.use_case.route_risk_assessment(route)