from sqlmodel import SQLModel, Field


class MyStocks(SQLModel, table=True):
    __tablename__ = "MyStocks"
    id: int | None = Field(default=None, primary_key=True)
    login_id: str = Field(index=True)
    quantity: int = Field(default=None)
    stock_name: str
