from sqlmodel import SQLModel, Field


class TradeStocks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    login_id: str
    stock_name: str
    is_buy: bool
    quantity: int = Field(default=None)
