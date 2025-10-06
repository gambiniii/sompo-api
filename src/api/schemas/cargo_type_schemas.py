from pydantic import BaseModel, Field
from typing import Optional


class CargoTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    theft: int = Field(..., ge=0)
    accident: int = Field(..., ge=0)
    irtc: int = Field(..., ge=0)
    global_risk_level: int = Field(..., ge=0)


class CargoTypeCreate(CargoTypeBase):
    pass


class CargoTypeOut(CargoTypeBase):
    id: int

    class Config:
        from_attributes = True


class CargoTypeParams(BaseModel):
    name: Optional[str] = None
    min_theft: Optional[int] = None
    max_theft: Optional[int] = None
    min_accident: Optional[int] = None
    max_accident: Optional[int] = None
    min_global_risk_level: Optional[int] = None
    max_global_risk_level: Optional[int] = None
    limit: int = 100
    offset: int = 0
