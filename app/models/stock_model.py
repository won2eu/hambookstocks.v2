from dataclasses import dataclass


@dataclass
class StockPriceResponse:
    stock_code: str
    timestamp: str
    current_price: str
