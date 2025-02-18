from pydantic import BaseModel # BaseModel 조필4
from app.models.user_models import User

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

class stock_to_buy_and_sell(BaseModel): #req 클래스
    stock_code: str
    stock_price: int | None = None
    quantity: int