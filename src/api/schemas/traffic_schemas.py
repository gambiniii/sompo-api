from datetime import date
from pydantic import BaseModel, Field, condecimal
from typing import Optional


class TrafficBase(BaseModel):
    date: date
    direction: str = Field(..., min_length=1, max_length=255)
    latitude: condecimal(max_digits=9, decimal_places=6)  # type: ignore
    longitude: condecimal(max_digits=9, decimal_places=6)  # type: ignore
    uf: int = Field(..., ge=0)
    highway: int = Field(..., ge=0)
    km: int = Field(..., ge=0)
    total: int = Field(..., ge=0)
    route_id: Optional[int] = None


class TrafficCreate(TrafficBase):
    pass


class TrafficOut(TrafficBase):
    id: int

    class Config:
        from_attributes = True


class TrafficParams(BaseModel):
    direction: Optional[str] = None
    uf: Optional[int] = None
    highway: Optional[int] = None
    route_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    min_lat: Optional[float] = None
    max_lat: Optional[float] = None
    min_lng: Optional[float] = None
    max_lng: Optional[float] = None
    limit: int = 100
    offset: int = 0
