from fastapi import APIRouter, Request, HTTPException
from src.api.controllers.risk import RiskController
from src.api.schemas.risk import RouteRequest

controller = RiskController()

risk_router = APIRouter(prefix="/risk", tags=["risks"])


@risk_router.post("/route/assessment")
async def assess_route_risk(route_data: RouteRequest):
    try:
        return controller.route_risk_assessment(route_data.route)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@risk_router.get("/{risk_id}")
def get_risk(risk_id: int):
    return {"risk_id": risk_id}
