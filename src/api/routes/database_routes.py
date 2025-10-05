from fastapi import APIRouter, HTTPException
from src.api.controllers.database_controller import DatabaseController

controller = DatabaseController()

database_router = APIRouter(prefix="/database", tags=["Databases"])


@database_router.post("/database/seed")
async def seed():
    try:
        return controller.seed()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
