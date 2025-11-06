from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from src.api.schemas.risk_schemas import RouteRiskResponse
from src.api.schemas.accident_risk_schemas import AccidentRouteRiskResponse


class SeparatedRouteRequest(BaseModel):
    route: List[Tuple[float, float]]
    expected_hour: int = Field(..., ge=0, le=23)
    weekday: int = Field(..., ge=0, le=6)
    cargo_type: str = Field(..., description="Descrição do tipo de carga da planilha unificada")
    weather_condition: Optional[str] = Field(None, description="Condição climática")


class CargoMapping(BaseModel):
    unified_cargo: str = Field(..., description="Tipo de carga da planilha unificada")
    theft_model_cargo: str = Field(..., description="Tipo de carga mapeado para modelo de roubo")
    accident_model_cargo: str = Field(..., description="Tipo de carga mapeado para modelo de acidente")
    note: str = Field(..., description="Nota explicativa sobre o mapeamento")


class SeparatedRouteRiskResponse(BaseModel):
    theft_risk: RouteRiskResponse
    accident_risk: AccidentRouteRiskResponse
    overall_risk_score: float
    overall_risk_category: str
    recommendations: List[str]
    cargo_mapping: CargoMapping = Field(..., description="Informação sobre mapeamento de cargas")
