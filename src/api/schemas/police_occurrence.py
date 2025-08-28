from datetime import date
from pydantic import BaseModel, Field, condecimal

class PoliceOccurrenceBase(BaseModel):
    police_occurrence_type_id: int = Field(..., ge=1)
    description: str = Field(..., min_length=1, max_length=255)
    lat: condecimal(max_digits=9, decimal_places=6) # type: ignore
    lng: condecimal(max_digits=9, decimal_places=6) # pyright: ignore[reportInvalidTypeForm]
    occurred_at: date
    h3_id: str = Field(..., min_length=1, max_length=20)

class TrafficOccurrenceCreate(PoliceOccurrenceBase):
    pass

class TrafficOccurrenceOut(PoliceOccurrenceBase):
    id: int
    class Config:
        from_attributes = True
