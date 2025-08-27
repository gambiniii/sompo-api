from fastapi import APIRouter

police_occurrence_router = APIRouter(prefix="/police_occurrence", tags=["police_occurrence"])

@police_occurrence_router.get("/")
def get_stock():
    return {"police_occurrence": ["funcionou"]}

@police_occurrence_router.get("/{stock_id}")
def get_stock(stock_id: int):
    return {"stock_id": stock_id}
