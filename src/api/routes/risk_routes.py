from fastapi import APIRouter, HTTPException
from src.api.controllers.risk_controller import RiskController
from src.api.schemas.risk_schemas import RouteRequest, RouteRiskResponse

controller = RiskController()

risk_router = APIRouter(prefix="/risk", tags=["risks"])

@risk_router.post("/route/assessment", response_model=RouteRiskResponse)
async def assess_route_risk(route_data: RouteRequest) -> RouteRiskResponse:
    """
    Avalia o risco de uma rota baseado em dados históricos de ocorrências.

    Retorna a porcentagem de risco (0-100%) para cada ponto da rota.
    """
    try:
        return controller.route_risk_assessment(
            route_data.route,
            route_data.expected_hour,
            route_data.weekday
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
