from sqlmodel import SQLModel, Field

class record(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    login_id: str = Field(index=True)
    quantity: int = Field(default=None)
    stock_code: str
    access_token: str | None = None
