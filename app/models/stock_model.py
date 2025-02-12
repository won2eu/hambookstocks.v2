from dataclasses import dataclass

@dataclass
class StockInfo:
    symbol: str
    current_price: float
    today_high: float
    today_low: float
    volume: int