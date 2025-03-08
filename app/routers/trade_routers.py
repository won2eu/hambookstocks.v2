from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.dependencies.db import get_db_session
from app.models.DB_user_models import User
from app.models.DB_mystocks_models import MyStocks
from app.models.parameter_models import stock_to_buy_and_sell
from app.dependencies.redis_db import get_redis
from sqlmodel import select
from app.models.DB_Market_stocks_models import MarketStocks
from app.models.DB_User_stocks_models import UserStocks
from app.services.trade_service import trade_service
from app.models.DB_trade_models import TradeStocks

router = APIRouter(prefix="/trade")


@router.post("/buy")  # req: 수량, 금액, 주식 코드
async def buy_stock(
    req: stock_to_buy_and_sell,
    db: Session = Depends(get_db_session),
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
    trade_service: trade_service = Depends(),
):

    # if not authorization:
    #     raise HTTPException(status_code=401, detail="로그인하셔야 합니다.")

    # token = authorization.split(" ")[1]

    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYSIsImxvZ2luX2lkIjoiYSIsImVtYWlsIjoiYSIsImlkIjoxLCJiYWxhbmNlIjo1MDEwMTYuMCwiZXhwIjoxNzQwOTkxNDQ5fQ.yUEp0N-1yWtTO2y8tbptQ76BboNFPGocMN9DmwxGLjo"

    if not (login_id := await redis_db.get(token)):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    user = db.exec(select(User).where(User.login_id == login_id)).first()

    # 토큰 인증은 끝

    # req.quantity가 0이 될때까지 사버리는거야
    stock_to_buy = db.exec(
        select(TradeStocks).where(
            TradeStocks.stock_name == req.stock_name and TradeStocks.is_buy == False
        )
    ).first()  # 여기서부터 수정하면 됨

    # 2. 돈이 있는지 없는지 확인하자
    total_price = req.stock_price
    if user.balance < total_price:
        raise HTTPException(status_code=400, detail="잔액이 부족합니다.")

    # 돈이 있으면 User의 산 가격만큼 돈을 줄이고

    change = user.balance - total_price
    db.query(User).filter(User.id == user.id).update({"balance": change})
    # 잔돈으로 새로 업데이트한 후에

    existing_stock = (
        db.query(MyStocks).filter(MyStocks.stock_name == req.stock_name).first()
    )

    if existing_stock:
        db.query(MyStocks).filter(MyStocks.stock_name == req.stock_name).update(
            {"quantity": MyStocks.quantity + req.quantity}
        )

        db.commit()
        # DB에 주식을 추가해준다

    else:
        new_stock = MyStocks(
            login_id=user.login_id,
            stock_name=req.stock_name,
            quantity=req.quantity,
        )
        db.add(new_stock)

    trade_service.update_buy(db, stock, req.quantity)
    trade_service.update_price(db, stock)

    db.commit()

    return {"msg": "구매 완료"}


@router.post("/sell")
async def sell_order(
    req: stock_to_buy_and_sell,
    db=Depends(get_db_session),
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
    trade_service: trade_service = Depends(),
):
    """토큰인증"""

    stock = db.exec(
        select(MarketStocks).where(MarketStocks.stock_name == req.stock_name)
    ).first()

    if not stock:
        stock = db.exec(
            select(UserStocks).where(UserStocks.stock_name == req.stock_name)
        ).first()

    # if not authorization:
    #     raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")
    # token = authorization.split(" ")[1]  # "Bearer <토큰>"에서 토큰만 추출
    # # table에 해당 토큰이 있는지 확인

    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmFtZSI6ImEiLCJlbWFpbCI6ImEiLCJsb2dpbl9pZCI6ImEiLCJiYWxhbmNlIjo0MzEwMDAuMCwiZXhwIjoxNzQwOTg5NTUzfQ.0KaHPgFukdxqcqk-YhrL76a0r_YeAmxlqW_co5SfSsY"

    if not (login_id := await redis_db.get(token)):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    user = db.exec(select(User).where(User.login_id == login_id)).first()

    """mystocks db의 내 보유주식 수량 차감"""
    # 보유주식 확인
    mystock = (
        db.query(MyStocks)
        .filter(
            MyStocks.login_id == user.login_id, MyStocks.stock_name == req.stock_name
        )
        .first()
    )

    if not mystock:
        raise HTTPException(status_code=404, detail="Not Found")

    if mystock.quantity > req.quantity:
        db.query(MyStocks).filter(
            MyStocks.login_id == user.login_id, MyStocks.stock_name == req.stock_name
        ).update({"quantity": MyStocks.quantity - req.quantity})

    elif mystock.quantity == req.quantity:
        db.delete(mystock)

    else:
        raise HTTPException(status_code=401, detail="너무 많아요")

    """현재 가치 불러와서 user db의 잔고에 돈 추가"""
    total_earned = req.stock_price
    db.query(User).filter(User.id == user.id).update(
        {"balance": User.balance + total_earned}
    )

    trade_service.update_sell(db, stock, req.quantity)
    trade_service.update_price(db, stock)

    db.commit()

    return {"msg": "매도 성공"}
