from pydantic import BaseModel  # BaseModel 조필4
from app.models.DB_user_models import User
from app.models.DB_User_stocks_models import UserStocks
from typing import Union


class AuthSigninReq(BaseModel):
    login_id: str
    pwd: str


class AuthSignupReq(BaseModel):
    login_id: str
    pwd: str
    name: str
    email: str


class AuthResp(BaseModel):
    message: str
    user: User
    access_token: str | None = None


class stock_to_buy_and_sell(BaseModel):  # req 클래스
    stock_name: str
    stock_price: float | None = None
    quantity: int


class MakeStockReq(BaseModel):
    stock_name: str
    stock_price: float
    stock_quantity: int
    stock_description: str


class MakeStockResp(BaseModel):
    userstock: UserStocks
    message: str


class MyPageResp(BaseModel):
    name: str
    login_id: str
    email: str
    balance: float


class ChangePwd(BaseModel):
    origin_pwd: str
    new_pwd: str
    check_new_pwd: str


class TradeStocksResp(BaseModel):
    stock_quantity: int
    is_buy: bool | None = None


class TradeStockReq(BaseModel):
    stock_name: str


class AllStocksResp(BaseModel):
    stock_level: Union[int, str]
    stock_description: Union[int, str]
