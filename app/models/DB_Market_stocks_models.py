from sqlmodel import SQLModel, Field


class MarketStocks(SQLModel, table=True):  # 고유 주식 종목들
    id: int | None = Field(default=None, primary_key=True)
    stock_name: str
    stock_price: float
    total_buy: int = Field(default=0)
    total_sell: int = Field(default=0)
