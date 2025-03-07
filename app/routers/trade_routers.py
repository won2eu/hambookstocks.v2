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

router = APIRouter(prefix="/trade")


@router.post("/buy")  # req: 수량, 금액, 주식 코드
def buy_stock(
    req: stock_to_buy_and_sell,
    db: Session = Depends(get_db_session),
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
):
    # DB에서 stock 고르기
    stock = db.exec(
        select(MarketStocks).where(MarketStocks.stock_name == req.stock_name)
    ).first()

    if not stock:
        stock = db.exec(
            select(UserStocks).where(UserStocks.stock_name == req.stock_name)
        ).first()

    if not authorization:
        raise HTTPException(status_code=401, detail="로그인하셔야 합니다.")

    token = authorization.split(" ")[1]

    if not (login_id := redis_db.get(token)):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    user = db.exec(select(User).where(User.login_id == login_id)).first()

    # 토큰 인증은 끝
    # 2. 돈이 있는지 없는지 확인하자자
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
    db.commit()

    return {"msg": "구매 완료"}


@router.post("/sell")
def sell_order(
    req: stock_to_buy_and_sell,
    db=Depends(get_db_session),
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
):
    """토큰인증"""

    if not authorization:
        raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")
    token = authorization.split(" ")[1]  # "Bearer <토큰>"에서 토큰만 추출
    # table에 해당 토큰이 있는지 확인

    if not (login_id := redis_db.get(token)):
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

    db.commit()

    """현재 가치 불러와서 user db의 잔고에 돈 추가"""
    total_earned = req.stock_price
    db.query(User).filter(User.id == user.id).update(
        {"balance": User.balance + total_earned}
    )
    db.commit()

    return {"msg": "매도 성공"}
