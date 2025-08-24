from pydantic import BaseModel
from typing import List, Tuple


class RouteRequest(BaseModel):
    route: List[Tuple[float, float]]  # (lat, lng)
