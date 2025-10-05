from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TrafficOccurrenceTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=255)

class PoliceOccurrenceTypeCreate(TrafficOccurrenceTypeBase):
    pass

class PoliceOccurrenceTypeOut(TrafficOccurrenceTypeBase):
    id: int

    class Config:
        from_attributes = True

class TrafficOccurrenceParams(BaseModel):
    type_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    h3_id: Optional[str] = None
    min_lat: Optional[float] = None
    max_lat: Optional[float] = None
    min_lng: Optional[float] = None
    max_lng: Optional[float] = None
    limit: int = 100
    offset: int = 0  
