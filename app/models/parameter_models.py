from pydantic import BaseModel
from app.models.user_models import User
from typing import List

class AuthSigninReq(BaseModel):
    login_id: str
    pwd: str

class AuthSignupReq(BaseModel):
    login_id: str
    pwd: str
    name: str

class AuthResp(BaseModel):
    message: str
    user: User
    access_token: str | None = None

class stock_to_buy(BaseModel): #req 클래스
    login_id : str
    stock_code: int
    stock_price: int | None = None
    quantity: int
