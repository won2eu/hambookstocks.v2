from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.parameter_models import MakeStockReq, MakeStockResp
from app.dependencies.db import get_db_session
from sqlmodel import Session, select, update
from app.models.DB_User_stocks_models import UserStocks
from app.dependencies.redis_db import get_redis
from app.models.DB_user_models import User

router = APIRouter(prefix="/mypage")


@router.post("/make_stock", response_model=MakeStockResp)
async def make_stock(
    req: MakeStockReq,
    db: Session = Depends(get_db_session),
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
):

    if not authorization:
        raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")
    token = authorization.split(" ")[1]

    if not (login_id := await redis_db.get(token)):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    # 주식 하나만 만들기 가능
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

    # 주식 상장시 내 balance 를 사용하기
    user = db.exec(select(User).where(User.login_id == login_id)).first()

    making_stock_price = req.stock_price * req.stock_quantity

    if user.balance < making_stock_price:
        raise HTTPException(status_code=400, detail="잔액이 부족합니다.")

    db.exec(
        update(User)
        .where(User.login_id == login_id)
        .values(balance=user.balance - making_stock_price)
    )
    db.commit()

    new_stock = UserStocks(
        login_id=login_id,
        stock_name=req.stock_name,
        stock_price=req.stock_price,
        stock_quantity=req.stock_quantity,
        stock_description=req.stock_description,
    )
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)

    return MakeStockResp(userstock=new_stock, message="나만의 주식 상장 성공!")
