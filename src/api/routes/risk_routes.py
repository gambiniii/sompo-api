from fastapi import APIRouter, HTTPException
from src.api.controllers.risk_controller import RiskController
from src.api.schemas.risk_schemas import RouteRequest, RouteRiskResponse

controller = RiskController()

risk_router = APIRouter(prefix="/risk", tags=["risks"])

@risk_router.post("/route/assessment", response_model=RouteRiskResponse)
async def assess_route_risk(route_data: RouteRequest) -> RouteRiskResponse:
    """
    Avalia o risco de uma rota baseado em dados históricos de ocorrências.

    Retorna análise completa de risco incluindo score, categoria e segmentos críticos.
    """
    try:
        return controller.route_risk_assessment(
            route_data.route,
            route_data.expected_hour,
            route_data.weekday,
            route_data.cargo_type
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
