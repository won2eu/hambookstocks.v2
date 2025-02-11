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

# class RecordResp(BaseModel):
#     message: str
#     records: List[Record]
#     # access_token: str | None = None
