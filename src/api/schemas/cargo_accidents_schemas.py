from datetime import date
from pydantic import BaseModel, Field, condecimal
from typing import Optional


class CargoAccidentsBase(BaseModel):
    date: date
    state: str = Field(..., min_length=2, max_length=2)
    highway: str = Field(..., min_length=1, max_length=255)
    kilometer: int = Field(..., ge=0)
    city: str = Field(..., min_length=1, max_length=255)
    accident_cause: str = Field(..., min_length=1, max_length=255)
    accident_type: str = Field(..., min_length=1, max_length=255)
    accident_classification: str = Field(..., min_length=1, max_length=255)
    day_period: str = Field(..., min_length=1, max_length=255)
    road_direction: str = Field(..., min_length=1, max_length=255)
    weather_condition: str = Field(..., min_length=1, max_length=255)
    road_type: str = Field(..., min_length=1, max_length=255)
    road_layout: str = Field(..., min_length=1, max_length=255)
    land_use: str = Field(..., min_length=1, max_length=255)
    people: int = Field(..., ge=0)
    deaths: int = Field(..., ge=0)
    minor_injuries: int = Field(..., ge=0)
    serious_injuries: int = Field(..., ge=0)
    unharmed: int = Field(..., ge=0)
    unknown: int = Field(..., ge=0)
    injured: int = Field(..., ge=0)
    vehicles: int = Field(..., ge=0)
    latitude: condecimal(max_digits=9, decimal_places=6)  # type: ignore
    longitude: condecimal(max_digits=9, decimal_places=6)  # type: ignore


class CargoAccidentsCreate(CargoAccidentsBase):
    pass


class CargoAccidentsOut(CargoAccidentsBase):
    id: int

    class Config:
        from_attributes = True


class CargoAccidentsParams(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    highway: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    accident_type: Optional[str] = None
    min_lat: Optional[float] = None
    max_lat: Optional[float] = None
    min_lng: Optional[float] = None
    max_lng: Optional[float] = None
    limit: int = 100
    offset: int = 0
