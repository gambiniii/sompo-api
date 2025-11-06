from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from src.api.schemas.risk_schemas import RouteRiskResponse
from src.api.schemas.accident_risk_schemas import AccidentRouteRiskResponse


class CombinedRouteRequest(BaseModel):
    route: List[Tuple[float, float]]  # (lat, lng)
    expected_hour: int = Field(..., ge=0, le=23)  # Hour of the day (0-23)
    weekday: int = Field(..., ge=0, le=6)  # Day of the week (0=Monday, 6=Sunday)
    cargo_type: str = Field(..., description="Tipo de carga")
    weather_condition: Optional[str] = Field(None, description="Condição climática (para risco de acidentes)")


class CombinedRouteRiskResponse(BaseModel):
    theft_risk: RouteRiskResponse = Field(..., description="Análise de risco de roubo")
    accident_risk: AccidentRouteRiskResponse = Field(..., description="Análise de risco de acidente")
    overall_risk_score: float = Field(..., description="Score de risco combinado (0-1)")
    overall_risk_category: str = Field(..., description="Categoria geral: BAIXO, MÉDIO, ALTO, CRÍTICO")
    recommendations: List[str] = Field(..., description="Recomendações baseadas nos riscos")
