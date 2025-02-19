from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.parameter_models import *
from app.models.mystocks_models import MyStocks
from app.dependencies.db import *
from sqlmodel import select
from app.dependencies.jwt_utils import *
from typing import Annotated


router = APIRouter()


@router.get("/mystocks")
def get_mystocks(
    Authorization: Annotated[str, Header()],
    jwtUtil: JWTUtil = Depends(),
    db=Depends(get_db_session),
):
    # 헤더로 온 토큰과 일치하는 유저의 mystocks를 가져온다.
    token = Authorization.replace("Bearer ", "")  # 헤더 요청의 토큰
    if not token:
        raise HTTPException(status_code=400, detail="Token is required")

    try:
        payload = jwtUtil.decode_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token decode error")

    login_id = payload.get("login_id")

    if login_id is None:
        raise HTTPException(status_code=400, detail="Login ID not found in token")

    mystocks = db.exec(select(MyStocks).where(MyStocks.login_id == login_id)).all()
    return {"message": "Mystocks found", "mystocks": mystocks}


@router.post("/gg")
def gg(
    Authorization: Annotated[str, Header()],
    jwtUtil: JWTUtil = Depends(),
    db=Depends(get_db_session),
):

    token = Authorization.replace("Bearer ", "")

    if not token:
        raise HTTPException(status_code=400, detail="Token is required")

    try:
        payload = jwtUtil.decode_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        raise HTTPException(status_code=401, detail="Token decode error")

    login_id = payload.get("login_id")

    if login_id is None:
        raise HTTPException(status_code=400, detail="Login ID not found in token")
    db.query(MyStocks).filter(MyStocks.login_id == login_id).delete()
    db.query(User).filter(User.login_id == login_id).update({"balance": 1000000})
    db.query(User).filter(User.login_id == login_id).update({"access_token": None})
    db.commit()

    return {"message": "gg"}
