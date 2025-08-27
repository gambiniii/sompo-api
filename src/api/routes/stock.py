from fastapi import APIRouter

stock_router = APIRouter(prefix="/stock", tags=["Items"])

@stock_router.get("/")
def get_stock():
    return {"paiva": "viado"}

@stock_router.get("/{stock_id}")
def get_stock(stock_id: int):
    return {"paiva": "viado"}
