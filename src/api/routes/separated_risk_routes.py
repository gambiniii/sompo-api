from fastapi import APIRouter, HTTPException
from src.api.controllers.separated_risk_controller import SeparatedRiskController
from src.api.schemas.separated_risk_schemas import SeparatedRouteRequest, SeparatedRouteRiskResponse

controller = SeparatedRiskController()

separated_risk_router = APIRouter(prefix="/separated-risk", tags=["separated-risks"])

@separated_risk_router.post("/route/assessment", response_model=SeparatedRouteRiskResponse)
async def assess_separated_route_risk(route_data: SeparatedRouteRequest) -> SeparatedRouteRiskResponse:
    """
    Avalia riscos de ROUBO e ACIDENTE separadamente com mapeamento automático de cargas.

    **Como funciona:**
    - Você envia o tipo de carga usando a nomenclatura de ROUBO
    - O sistema automaticamente mapeia para o tipo correspondente em ACIDENTES
    - Ambos os modelos são executados com os tipos corretos

    **Exemplo:**
    - Entrada: cargo_type="Medicamentos" (modelo de roubo)
    - Mapeamento automático: "Tóxicos/ Oxidantes" (modelo de acidentes)
    - Resultado: Ambas análises com tipos corretos
    """
    try:
        return controller.separated_risk_assessment(
            route_data.route,
            route_data.expected_hour,
            route_data.weekday,
            route_data.cargo_type,
            route_data.weather_condition
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
