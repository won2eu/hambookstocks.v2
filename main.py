
from fastapi import FastAPI, Depends, HTTPException
from dataclasses import dataclass
from sqlmodel import Field, SQLModel, create_engine, Session
from pydantic import BaseModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    login_id: str = Field(index=True)
    pwd: str = Field(default=None, exclude=True) # exclude: 백엔드 내부에서만 사용, 사용자에게 제공 X
    name: str
    # access_token: str | None = None

class AuthSigninReq(BaseModel):
    login_id: str
    pwd: str
    
class AuthResp(BaseModel):
    message: str
    user: User
    # access_token: str | None = None

app = FastAPI()

DB_URL = "sqlite:///user.db"
# DB_PWD = "dbdbd"
DB_ENGINE = create_engine(DB_URL, connect_args={"check_same_thread": False})

def get_db_session():
    with Session(DB_ENGINE) as session:
        yield session
def create_db_and_tables():
    SQLModel.metadata.create_all(DB_ENGINE)

create_db_and_tables()

@app.post('/auth/login')
def login(req: AuthSigninReq,
          db=Depends(get_db_session)):
    user = db.query(User).filter(User.login_id == req.login_id).first()

    if not user or user.pwd != req.pwd:
        raise HTTPException(status_code=401, detail="Login failed")
    
    return AuthResp(
        message="Login success",
        user=user
        # access_token=user.access_token
    )