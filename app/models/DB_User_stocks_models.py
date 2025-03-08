from sqlmodel import SQLModel, Field


class UserStocks(SQLModel, table=True):  # 유저가 만든 주식 종목들
    id: int | None = Field(default=None, primary_key=True)
    login_id: str
    stock_name: str
    stock_price: float
    trend_buy: int = Field(default=0)
    trend_sell: int = Field(default=0)
    total_buy: int = Field(default=0)
    total_sell: int = Field(default=0)
    stock_level: int = Field(default=1)
    stock_description: str
