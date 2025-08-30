from pydantic import BaseModel, Field
from typing import Optional

class TrafficOccurrenceTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=255)

class PoliceOccurrenceTypeCreate(TrafficOccurrenceTypeBase):
    pass

class PoliceOccurrenceTypeOut(TrafficOccurrenceTypeBase):
    id: int

    class Config:
        from_attributes = True  
