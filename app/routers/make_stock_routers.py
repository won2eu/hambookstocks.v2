from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.parameter_models import MakeStockReq, MakeStockResp
from app.models.DB_User_stocks_models import UserStocks
from app.dependencies.db import get_db_session
from sqlmodel import Session, select
from app.dependencies.redis_db import get_redis
from app.models.DB_user_models import User

router = APIRouter()

making_stock_price = 30000  # 주식 상장하는데 드는 비용


@router.post("/make_stock", response_model=MakeStockResp)
async def make_stock(
    req: MakeStockReq,
    db: Session = Depends(get_db_session),
    redis_db=Depends(get_redis),
    authorization: str = Header(None),
):

    # if not authorization:
    #     raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")

    # token = authorization.split(" ")[1]
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbl9pZCI6ImEiLCJuYW1lIjoiYSIsImVtYWlsIjoiYSIsImJhbGFuY2UiOjgxMDE2LjAsImlkIjoxLCJleHAiOjE3NDA5OTY3NDN9.39wzIkWDxA_4mC_-igz1cBkqv7POYEjT5KPzRA8L3pg"

    if not (login_id := await redis_db.get(token)):
        raise HTTPException(status_code=404, detail="로그인이 필요합니다.")

    # 해당 유저가 이미 만든 주식이 있다면 에러
    existing_stock = db.exec(
        select(UserStocks).where(UserStocks.login_id == login_id)
    ).first()
    if existing_stock:
        raise HTTPException(status_code=400, detail="이미 만든 주식이 존재합니다.")

    # 만드려는 주식 이름이 DB에 중복된다면 에러
    duplicate_stock = db.exec(
        select(UserStocks).where(UserStocks.stock_name == req.stock_name)
    ).first()
    if duplicate_stock:
        raise HTTPException(status_code=400, detail="이미 존재하는 주식 이름입니다.")

    user = db.exec(select(User).where(User.login_id == login_id)).first()

    if user.balance < making_stock_price:
        raise HTTPException(status_code=400, detail="잔액이 부족합니다.")

    change = user.balance - making_stock_price
    user.balance = change

    db.commit()
    db.refresh(user)

    new_stock = UserStocks(
        login_id=login_id,
        stock_name=req.stock_name,
        stock_price=req.stock_price,
        stock_description=req.stock_description,
    )

    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)

    return MakeStockResp(userstock=new_stock, message="주식 상장 성공.")
