from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.parameter_models import *
from app.models.DB_mystocks_models import MyStocks
from app.dependencies.redis_db import get_redis
from app.dependencies.db import *
from sqlmodel import select
from app.dependencies.jwt_utils import *
from typing import Annotated


router = APIRouter()


@router.get("/mystocks")
async def get_mystocks(
    authorization: Annotated[str, Header()],
    db=Depends(get_db_session),
    redis_db=Depends(get_redis),
):
    # 헤더로 온 토큰과 일치하는 유저의 mystocks를 가져온다.
    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="토큰이 필요합니다.")

    login_id = await redis_db.get(token)
    if not login_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    # redis에서 가져온 값이 byte 타입 일 수도 있음.
    login_id = login_id.decode("utf-8")

    if login_id is None:
        raise HTTPException(status_code=400, detail="Login ID not found in token")

    mystocks = db.exec(select(MyStocks).where(MyStocks.login_id == login_id)).all()
    return {"message": "Mystocks found", "mystocks": mystocks}
