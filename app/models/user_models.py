from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "Users"
    id: int | None = Field(default=None, primary_key=True)
    login_id: str = Field(index=True)
    pwd: str = Field(default=None, exclude=True)
    name: str
    email: str
    balance: float = Field(default=0.0)  # foriegn key 적용
