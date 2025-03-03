from sqlmodel import SQLModel, Field


class MarketStocks(SQLModel, table=True):
    stock_name: str
    stock_price: float
    trend_buy: int = Field(default=0)
    trend_sell: int = Field(default=0)
    total_buy: int = Field(default=0)
    total_sell: int = Field(default=0)
