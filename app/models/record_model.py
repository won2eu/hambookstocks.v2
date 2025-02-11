from sqlmodel import SQLModel, Field

class record(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    login_id: str = Field(index=True)
    profit_rate: float = Field(index=True)
