from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    login_id: str = Field(index=True)
    pwd: str = Field(default=None, exclude=True)
    name: str
    #access_token: str | None = None
