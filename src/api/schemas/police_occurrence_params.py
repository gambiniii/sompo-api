from typing import Optional
from datetime import date
from pydantic import BaseModel, Field


class PoliceOccurrenceParams(BaseModel):
    """
    Representa os parâmetros de consulta para ocorrências policiais.
    """
    type_id: Optional[int] = Field(None, description="ID do tipo de ocorrência.")
    h3_id: Optional[str] = Field(None, description="ID da célula H3.")
    start_date: Optional[date] = Field(None, description="Data de início para a busca.")
    end_date: Optional[date] = Field(None, description="Data de fim para a busca.")
    min_lat: Optional[float] = Field(None, description="Latitude mínima.")
    max_lat: Optional[float] = Field(None, description="Latitude máxima.")
    min_lng: Optional[float] = Field(None, description="Longitude mínima.")
    max_lng: Optional[float] = Field(None, description="Longitude máxima.")
    limit: int = Field(100, ge=1, le=1000, description="Limite de resultados (entre 1 e 1000).")
    offset: int = Field(0, ge=0, description="Número de resultados a serem pulados.")