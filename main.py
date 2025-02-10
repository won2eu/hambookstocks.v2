from fastapi import FastAPI, Depends, HTTPException
from app.models.parameter_models import *
from pydantic import BaseModel
from app.models.user_models import User
from app.dependencies.db import *

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