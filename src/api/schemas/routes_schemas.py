from pydantic import BaseModel, Field
from typing import Optional


class RoutesBase(BaseModel):
    route: str = Field(..., min_length=1, max_length=255)
    highway: str = Field(..., min_length=1, max_length=255)
    total_traffic: int = Field(..., ge=0)


class RoutesCreate(RoutesBase):
    pass


class RoutesOut(RoutesBase):
    id: int

    class Config:
        from_attributes = True


class RoutesParams(BaseModel):
    route: Optional[str] = None
    highway: Optional[str] = None
    min_total_traffic: Optional[int] = None
    max_total_traffic: Optional[int] = None
    limit: int = 100
    offset: int = 0
