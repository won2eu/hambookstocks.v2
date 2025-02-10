from fastapi import APIRouter, HTTPException
from app.services.stock_service import get_stock_info
from app.models.stock_model import StockInfo

router = APIRouter(
    prefix = '/stocks'
)

@router.get("/{symbol}", response_model=StockInfo)
async def get_stock(symbol: str):
    try:
        stock_info = get_stock_info(symbol)
        return stock_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
