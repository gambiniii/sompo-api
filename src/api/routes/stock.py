from fastapi import APIRouter

stock_router = APIRouter(prefix="/stock", tags=["Items"])

@stock_router.get("/")
def get_stock():
    return {"stock": ["stock1", "stock2"]}

@stock_router.get("/{stock_id}")
def get_stock(stock_id: int):
    return {"stock_id": stock_id}
