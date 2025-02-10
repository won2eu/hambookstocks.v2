from fastapi import FastAPI, Depends, HTTPException
from app.models.parameter_models import *
from pydantic import BaseModel
from app.models.user_models import User
from app.dependencies.db import *

app = FastAPI()

create_db_and_table()

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

@app.post('/auth/logout')
def auth_logout():
    #토큰 삭제 로직 추가해야함 (프론트?)
    #로그아웃시 로그인 html로 이동
    return {
        "message" : "로그아웃 되었습니다."
    }