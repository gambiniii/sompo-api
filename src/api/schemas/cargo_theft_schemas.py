from datetime import date
from pydantic import BaseModel, Field, condecimal
from typing import Optional


class CargoTheftBase(BaseModel):
    state: str = Field(..., min_length=2, max_length=2)
    city: str = Field(..., min_length=1, max_length=255)
    neighborhood: str = Field(..., min_length=1, max_length=255)
    street: str = Field(..., min_length=1, max_length=255)
    lat: condecimal(max_digits=9, decimal_places=6)  # type: ignore
    lng: condecimal(max_digits=9, decimal_places=6)  # type: ignore
    occurred_at: date


class CargoTheftCreate(CargoTheftBase):
    pass


class CargoTheftOut(CargoTheftBase):
    id: int

    class Config:
        from_attributes = True


class CargoTheftParams(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    min_lat: Optional[float] = None
    max_lat: Optional[float] = None
    min_lng: Optional[float] = None
    max_lng: Optional[float] = None
    limit: int = 100
    offset: int = 0
