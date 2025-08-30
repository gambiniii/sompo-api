from pydantic import BaseModel, Field
from typing import List, Tuple


class RouteRequest(BaseModel):
    route: List[Tuple[float, float]]  # (lat, lng)
    expected_hour: int = Field(..., ge=0, le=23)  # Hour of the day (0-23)
    weekday: int = Field(..., ge=0, le=6)  # Day of the week (0=Monday, 6=Sunday)
