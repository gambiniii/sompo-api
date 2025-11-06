from fastapi import APIRouter, HTTPException
from src.api.controllers.accident_risk_controller import AccidentRiskController
from src.api.schemas.accident_risk_schemas import AccidentRouteRequest, AccidentRouteRiskResponse

controller = AccidentRiskController()

accident_risk_router = APIRouter(prefix="/accident-risk", tags=["accident-risks"])

@accident_risk_router.post("/route/assessment", response_model=AccidentRouteRiskResponse)
async def assess_accident_route_risk(route_data: AccidentRouteRequest) -> AccidentRouteRiskResponse:
    """
    Avalia o risco de acidentes em uma rota baseado em dados históricos.

    Retorna análise completa incluindo score, categoria, fatores climáticos e segmentos críticos.
    """
    try:
        return controller.route_risk_assessment(
            route_data.route,
            route_data.expected_hour,
            route_data.weekday,
            route_data.cargo_type,
            route_data.weather_condition
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
