from fastapi import FastAPI, Depends, HTTPException
from app.models.parameter_models import *
from pydantic import BaseModel
from app.models.user_models import User
from app.dependencies.db import *
from app.dependencies.jwt_utils import JWTUtil
from app.services.auth_service import AuthService

import os
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

create_db_and_table()

# 프론트 연결
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/login")

@app.get("/{page_name}", response_class=HTMLResponse)
async def get_page(page_name: str = "login"):
    page_path = f"frontend/{page_name}.html"
    if os.path.exists(page_path):
        with open(page_path, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="페이지를 찾을 수 없습니다.", status_code=404)


@app.post('/auth/login')
def login(req: AuthSigninReq,
          db=Depends(get_db_session)):
    
    user = db.query(User).filter(User.login_id == req.login_id).first()
#회원가입
@app.post('/auth/register', response_model=AuthResp)
def register(req: AuthSignupReq, db=Depends(get_db_session),
             jwtUtil: JWTUtil = Depends(),
             authService: AuthService = Depends()):
    existing_user = db.query(User).filter(User.login_id == req.login_id).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="ID already exists")

    new_user = authService.signup(db,req.login_id, req.pwd, req.name)

    if not new_user:
        raise HTTPException(status_code=400, detail="not found")
    
    return AuthResp(
        message= "User registered successfully",
        user = new_user
    )


#로그인
@app.post('/auth/login')
def login(req: AuthSigninReq,
          db=Depends(get_db_session), jwtUtil: JWTUtil = Depends(),
          authService: AuthService = Depends()):
    
    user = authService.signin(db,req.login_id,req.pwd)
    if not user:
        raise HTTPException(status_code=401, detail="Login failed")
    
    user.access_token = jwtUtil.create_token(user.model_dump())
    return AuthResp(
        message="로그인 되었습니다.",
        user=user,
        access_token=user.access_token
    )

#로그아웃
@app.post('/auth/logout')
def auth_logout():
    #토큰 삭제 로직 추가해야함 (프론트?)
    #로그아웃시 로그인 html로 이동
    return {
        "message" : "로그아웃 되었습니다."
    }