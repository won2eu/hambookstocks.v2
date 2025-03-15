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
from app.services.redis_service import RedisService

router = APIRouter(prefix="/trade")

alpha = 0.5  # 주식 가격 변동계수


@router.post("/buy")  # req: 수량, 금액, 주식 코드
async def buy_stock(
    req: stock_to_buy_and_sell,
    db: Session = Depends(get_db_session),
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
    trade_service: trade_service = Depends(),
    redis_service: RedisService = Depends(),
):

    # if not authorization:
    #     raise HTTPException(status_code=401, detail="로그인하셔야 합니다.")

    # token = authorization.split(" ")[1]

    token = ""

    if not (login_id := await redis_db.get(token)):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    # 토큰 인증은 끝

    # 0. 돈이 있는지 확인하고 돈이 없으면 구매불가능
    user = db.exec(select(User).where(User.login_id == login_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저가 없습니다.")

    if user.balance < req.stock_price * req.quantity:
        raise HTTPException(status_code=400, detail="돈이 부족합니다.")

    # 1. SELL_REQUEST 올라온거를 TRADE_STOCKS에서 찾고 찾는 수량보다 적게
    # 있으면 있는 만큼 구매하고 없는 만큼 BUY_REQUEST를 TRADESTOCKS에 올린다.
    trade_info = db.exec(
        select(TradeStocks).where(TradeStocks.stock_name == req.stock_name)
    ).first()
    seller = db.exec(select(User).where(User.login_id == trade_info.login_id)).first()

    # trade_info가 없으면 주식 매수 요청을 새로 올림
    if not trade_info:
        trade_info = TradeStocks(
            login_id=user.login_id,
            stock_name=req.stock_name,
            is_buy=True,
            quantity=req.quantity,
        )
        db.add(trade_info)

    if trade_info.is_buy:  # 매수 요청이 있으면
        trade_info.quantity += req.quantity

    else:  # 매수 요청이 없으면
        if trade_info.quantity > req.quantity:  # 요청 수보다 많으면 수량 차감
            available_quantity = req.quantity
            trade_info.quantity -= req.quantity

        if trade_info.quantity == req.quantity:  # 요청 수와 같으면 삭제
            available_quantity = req.quantity
            db.delete(trade_info)

        if (
            trade_info.quantity < req.quantity
        ):  # 요청 수보다 적으면 있는걸 다 차감하고 남은 수량만큼 매수 요청 올림
            available_quantity = trade_info.quantity
            trade_info.quantity = req.quantity - trade_info.quantity
            trade_info.is_buy = True

    db.commit()

    # 2. TRADE_STOCKS에서 해당 종목의 is_buy와 qunatity를 불러와서 가격 변동을 해서 해당 주식 종목의 가격에 새로 업데이트해
    updated_trade_info = db.exec(
        select(TradeStocks).where(TradeStocks.stock_name == req.stock_name)
    ).first()

    if updated_trade_info.is_buy == True:
        new_stock_price = req.stock_price + updated_trade_info.quantity * alpha
    else:
        new_stock_price = req.stock_price - updated_trade_info.quantity * alpha

    updated_stock_for_price = db.exec(
        select(UserStocks).where(UserStocks.stock_name == req.stock_name)
    ).first()

    if not updated_stock_for_price:
        updated_stock_for_price = db.exec(
            select(MarketStocks).where(MarketStocks.stock_name == req.stock_name)
        ).first()

    updated_stock_for_price.stock_price = new_stock_price

    # 3. REDIS에 가격을 저장 같이 해주기
    redis_service.update_stock(redis_db, req.stock_name, new_stock_price)

    # 4.구매한 USER의 BALANCE 차감과 보유주식에 추가
    user.balance -= req.stock_price * available_quantity
    buyer_stock = db.exec(
        select(MyStocks).where(
            MyStocks.login_id == user.login_id, MyStocks.stock_name == req.stock_name
        )
    ).first()

    if not buyer_stock:
        buyer_stock = MyStocks(
            login_id=user.login_id,
            stock_name=req.stock_name,
            quantity=available_quantity,
        )
        db.add(buyer_stock)
    else:
        buyer_stock.quantity += available_quantity

    # 5 판매한 USER의 BALANCE 증가와 보유주식에서 차감
    seller.balance += req.stock_price * available_quantity
    seller_stock = db.exec(
        select(MyStocks).where(
            MyStocks.login_id == seller.login_id, MyStocks.stock_name == req.stock_name
        )
    ).first()

    if not seller_stock:
        seller_stock = MyStocks(
            login_id=seller.login_id,
            stock_name=req.stock_name,
            quantity=available_quantity,
        )
        db.add(seller_stock)
    else:
        seller_stock.quantity -= available_quantity

    db.commit()

    return {"msg": "구매 완료"}


@router.post("/sell")
async def sell_order(
    req: stock_to_buy_and_sell,
    db=Depends(get_db_session),
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
    trade_service: trade_service = Depends(),
    redis_service: RedisService = Depends(),
):
    """토큰인증"""

    # if not authorization:
    #     raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")
    # token = authorization.split(" ")[1]  # "Bearer <토큰>"에서 토큰만 추출
    # # table에 해당 토큰이 있는지 확인

    token = ""

    if not (login_id := await redis_db.get(token)):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    # 토큰 인증 끝 ...

    # 0. 주식이 있는지 확인하고 주식이 없으면 판매불가능
    user = db.exec(select(User).where(User.login_id == login_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저가 없습니다.")
    seller_stock = db.exec(
        select(MyStocks).where(
            MyStocks.login_id == user.login_id, MyStocks.stock_name == req.stock_name
        )
    ).first()
    if not seller_stock:
        raise HTTPException(status_code=404, detail="보유주식이 없습니다.")

    if seller_stock.quantity < req.quantity:
        raise HTTPException(status_code=400, detail="보유주식이 부족합니다.")

    # 1. BUY_REQUEST 올라온거를 TRADE_STOCKS에서 찾고 찾는 수량보다 적게
    # 있으면 있는 만큼 판매하고 없는 만큼 SELL_REQUEST를 TRADESTOCKS에 올린다.
    trade_info = db.exec(
        select(TradeStocks).where(TradeStocks.stock_name == req.stock_name)
    ).first()
    buyer = db.exec(select(User).where(User.login_id == trade_info.login_id)).first()

    # trade_info가 없으면 주식 매도 요청을 새로 올림
    if not trade_info:
        trade_info = TradeStocks(
            login_id=user.login_id,
            stock_name=req.stock_name,
            is_buy=False,
            quantity=req.quantity,
        )
        db.add(trade_info)

    if not trade_info.is_buy:  # 매도 요청이 있으면
        trade_info.quantity += req.quantity

    else:  # 매도 요청이 없으면
        if trade_info.quantity > req.quantity:  # 요청 수보다 많으면 수량 차감
            available_quantity = req.quantity
            trade_info.quantity -= req.quantity

        if trade_info.quantity == req.quantity:  # 요청 수와 같으면 삭제
            available_quantity = req.quantity
            db.delete(trade_info)

        if (
            trade_info.quantity < req.quantity
        ):  # 요청 수보다 적으면 있는걸 다 차감하고 남은 수량만큼 매도 요청 올림
            available_quantity = trade_info.quantity
            trade_info.quantity = req.quantity - trade_info.quantity
            trade_info.is_buy = False

    db.commit()

    # 2. TRADE_STOCKS에서 해당 종목의 is_buy와 qunatity를 불러와서 가격 변동을 해서 해당 주식 종목의 가격에 새로 업데이트해
    updated_trade_info = db.exec(
        select(TradeStocks).where(TradeStocks.stock_name == req.stock_name)
    ).first()

    if updated_trade_info.is_buy == True:
        new_stock_price = req.stock_price + updated_trade_info.quantity * alpha
    else:
        new_stock_price = req.stock_price - updated_trade_info.quantity * alpha

    updated_stock_for_price = db.exec(
        select(UserStocks).where(UserStocks.stock_name == req.stock_name)
    ).first()

    if not updated_stock_for_price:
        updated_stock_for_price = db.exec(
            select(MarketStocks).where(MarketStocks.stock_name == req.stock_name)
        ).first()

    updated_stock_for_price.stock_price = new_stock_price

    # 3. REDIS에 가격을 저장 같이 해주기
    redis_service.update_stock(redis_db, req.stock_name, new_stock_price)

    # 4.구매한 USER의 BALANCE 차감과 보유주식에 추가

    buyer.balance -= req.stock_price * available_quantity
    buyer_stock = db.exec(
        select(MyStocks).where(
            MyStocks.login_id == buyer.login_id, MyStocks.stock_name == req.stock_name
        )
    ).first()

    if not buyer_stock:
        buyer_stock = MyStocks(
            login_id=buyer.login_id,
            stock_name=req.stock_name,
            quantity=available_quantity,
        )
        db.add(buyer_stock)
    else:
        buyer_stock.quantity += available_quantity

    # 5 판매한 USER의 BALANCE 증가와 보유주식에서 차감
    user.balance += req.stock_price * available_quantity
    seller_stock = db.exec(
        select(MyStocks).where(
            MyStocks.login_id == user.login_id, MyStocks.stock_name == req.stock_name
        )
    ).first()

    if not seller_stock:
        seller_stock = MyStocks(
            login_id=user.login_id,
            stock_name=req.stock_name,
            quantity=available_quantity,
        )
        db.add(seller_stock)
    else:
        seller_stock.quantity -= available_quantity

    db.commit()

    return {"msg": "매도 성공"}
