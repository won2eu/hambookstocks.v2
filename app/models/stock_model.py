from pydantic import BaseModel

class StockPriceResponse(BaseModel):
    stock_code: str
    timestamp: str
    current_price: str
