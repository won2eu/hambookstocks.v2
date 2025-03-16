from sqlmodel import SQLModel, Field


class UserStocks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    login_id: str
    stock_name: str
    stock_price: float
    stock_quantity: int = Field(default=0)
    total_buy: int = Field(default=0)
    total_sell: int = Field(default=0)
    stock_level: int = Field(default=1)
    stock_description: str
