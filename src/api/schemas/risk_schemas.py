from pydantic import BaseModel, Field
from typing import List, Tuple, Any, Dict


class RouteRequest(BaseModel):
    route: List[Tuple[float, float]]  # (lat, lng)
    expected_hour: int = Field(..., ge=0, le=23)  # Hour of the day (0-23)
    weekday: int = Field(..., ge=0, le=6)  # Day of the week (0=Monday, 6=Sunday)


class RiskPoint(BaseModel):
    latitude: float = Field(..., description="Latitude do ponto")
    longitude: float = Field(..., description="Longitude do ponto")
    log_score: float = Field(..., description="Score logarítmico do modelo KDE")
    normalized_log: float = Field(..., description="Score normalizado (0-1) para heatmap")
    risk_score_norm: float = Field(..., description="Score de risco normalizado (0-1)")
    risk_percentage: float = Field(..., description="Porcentagem de risco (0-100%)", ge=0, le=100)


class RouteRiskResponse(BaseModel):
    results: List[RiskPoint] = Field(..., description="Análise de risco por ponto da rota")
    average_log_density: float = Field(..., description="Densidade logarítmica média")
    average_normalized: float = Field(..., description="Score normalizado médio")
    points_analyzed: int = Field(..., description="Número de pontos analisados")
    confidence: float = Field(..., description="Nível de confiança da análise")
