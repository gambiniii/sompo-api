from fastapi import APIRouter, HTTPException
from src.api.controllers.combined_risk_controller import CombinedRiskController
from src.api.schemas.combined_risk_schemas import CombinedRouteRequest, CombinedRouteRiskResponse

controller = CombinedRiskController()

combined_risk_router = APIRouter(prefix="/combined-risk", tags=["combined-risks"])

@combined_risk_router.post("/route/assessment", response_model=CombinedRouteRiskResponse)
async def assess_combined_route_risk(route_data: CombinedRouteRequest) -> CombinedRouteRiskResponse:
    """
    Avalia AMBOS os riscos (roubo e acidente) em uma rota.

    Retorna análise completa com:
    - Risco de roubo (baseado em dados históricos de roubos)
    - Risco de acidentes (baseado em dados históricos de acidentes + clima)
    - Score de risco combinado
    - Recomendações personalizadas
    """
    try:
        return controller.combined_risk_assessment(
            route_data.route,
            route_data.expected_hour,
            route_data.weekday,
            route_data.cargo_type,
            route_data.weather_condition
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
