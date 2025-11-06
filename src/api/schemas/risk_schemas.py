from pydantic import BaseModel, Field, ConfigDict
from typing import List, Tuple, Any, Dict, Optional


class RouteRequest(BaseModel):
    route: List[Tuple[float, float]]  # (lat, lng)
    expected_hour: int = Field(..., ge=0, le=23)  # Hour of the day (0-23)
    weekday: int = Field(..., ge=0, le=6)  # Day of the week (0=Monday, 6=Sunday)
    cargo_type: str = Field(default="Cargas Fracionadas", description="Tipo de carga")


class CriticalSegment(BaseModel):
    segment_index: int
    latitude: float
    longitude: float
    risk_level: float
    risk_percentage: float


class RouteRiskResponse(BaseModel):
    model_config = ConfigDict(extra='allow')

    risk_score: float = Field(..., description="Score de risco ajustado (0-1)")
    base_risk: float = Field(..., description="Risco base antes do fator de carga")
    cargo_factor: float = Field(..., description="Fator multiplicador da carga")
    cargo_type: str = Field(..., description="Tipo de carga analisado")
    spatial_risk_avg: float = Field(..., description="Risco espacial médio")
    spatial_risk_max: float = Field(..., description="Risco espacial máximo")
    temporal_multiplier: float = Field(..., description="Multiplicador temporal")
    risk_category: str = Field(..., description="Categoria do risco: BAIXO, MÉDIO, ALTO, CRÍTICO")
    critical_segments: List[CriticalSegment] = Field(..., description="Segmentos críticos da rota")
    route_length_km: float = Field(..., description="Comprimento estimado da rota em km")
    departure_datetime: str = Field(..., description="Data/hora de partida")
