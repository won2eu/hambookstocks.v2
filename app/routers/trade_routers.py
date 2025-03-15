from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.dependencies.db import get_db_session
from app.models.DB_user_models import User
from app.models.DB_mystocks_models import MyStocks
from app.models.DB_trade_models import TradeStocks
from app.models.DB_Market_stocks_models import MarketStocks
from app.models.DB_User_stocks_models import UserStocks
from app.models.parameter_models import stock_to_buy_and_sell
from app.dependencies.redis_db import get_redis
from app.services.trade_service import TradeService
from app.services.redis_service import RedisService
from sqlmodel import select

router = APIRouter(prefix="/trade")
# 주식 가격변동계수
alpha = 100
available_quantity = 0  # 기본값으로 초기화


@router.post("/buy")  # req: 수량, 금액, 주식 코드,
async def buy_stock(
    req: stock_to_buy_and_sell,
    db: Session = Depends(get_db_session),
    # authorization: str = Header(None),
    redis_db=Depends(get_redis),
    trade_service: TradeService = Depends(),
    redis_service: RedisService = Depends(),
):
    # if not authorization:
    #     raise HTTPException(status_code=401, detail="로그인하셔야 합니다.")

    # token = authorization.split(" ")[1]
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiXHVhZTQwXHViYmZjXHVjYzJjIiwiaWQiOjQsImVtYWlsIjoia2ltbWMzNDIzQG5hdmVyLmNwbSIsImxvZ2luX2lkIjoiYWEiLCJiYWxhbmNlIjo5OTAwMDAuMCwiZXhwIjoxNzQyMDMwMDQ3fQ.XqG3Ts22XlQSnp0BrOazEG-AMHvrhdkrqmiJsBIol2o"
    if not (login_id := await redis_db.get(token)):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    """
    돈 있는지 확인 / 돈 없으면 구매 불가능
    """
    user = db.exec(select(User).where(User.login_id == login_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    if user.balance < req.quantity * req.stock_price:
        raise HTTPException(status_code=400, detail="잔액이 부족합니다.")

    """
    sell_req 올라온거 trade_stocks에서 찾고, 찾는 수량보다 적게 있으면.. 있는 만큼 구매하고, 없는 만큼 buy_req 를 tradestocks에 올린다
    """
    trade_info = db.exec(
        select(TradeStocks).where(TradeStocks.stock_name == req.stock_name)
    ).first()
    transaction_occurred = False
    seller = None

    if trade_info:
        if trade_info.is_buy:
            if trade_info.login_id == login_id:
                # 동일한 login_id인 경우 수량만 업데이트
                trade_info.quantity += req.quantity
            else:
                # 다른 login_id인 경우 새로운 요청 추가
                trade_info = TradeStocks(
                    login_id=login_id,
                    stock_name=req.stock_name,
                    is_buy=True,
                    quantity=req.quantity,
                )
                db.add(trade_info)
        else:
            # 판매 요청이 올라와 있으면
            seller = db.exec(
                select(User).where(User.login_id == trade_info.login_id)
            ).first()
            if trade_info.quantity > req.quantity:
                available_quantity = req.quantity
                trade_info.quantity -= req.quantity
                transaction_occurred = True
            elif trade_info.quantity == req.quantity:
                available_quantity = req.quantity
                db.delete(trade_info)
                transaction_occurred = True
            else:
                available_quantity = trade_info.quantity
                trade_info.quantity = req.quantity - trade_info.quantity
                trade_info.is_buy = True
                trade_info.login_id = login_id
                transaction_occurred = True
    else:
        # trade_info가 없으면 새로운 매수 요청 추가
        trade_info = TradeStocks(
            login_id=login_id,
            stock_name=req.stock_name,
            is_buy=True,
            quantity=req.quantity,
        )
        db.add(trade_info)

    db.commit()

    """
    구매한 user balance 차감, Mystocks 에 보유주식 추가
    판매한 user balance 증가, Mystocks 에 보유주식 감소
    """
    if transaction_occurred and seller:
        # 거래가 발생한 경우에만 사용자 잔액 및 주식 수량 업데이트
        seller.balance += available_quantity * req.stock_price
        user.balance -= available_quantity * req.stock_price
        buyer_stock = db.exec(
            select(MyStocks).where(
                MyStocks.login_id == login_id, MyStocks.stock_name == req.stock_name
            )
        ).first()
        if not buyer_stock:
            buyer_stock = MyStocks(
                login_id=login_id,
                stock_name=req.stock_name,
                quantity=available_quantity,
            )
            db.add(buyer_stock)
        else:
            buyer_stock.quantity += available_quantity

        seller_stock = db.exec(
            select(MyStocks).where(
                MyStocks.login_id == seller.login_id,
                MyStocks.stock_name == req.stock_name,
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

    """
    tradestocks 에 is_buy 인것과 quantity 를 불러온걸 활용해서 가격변동
    """
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
    db.commit()
    """
    변동된 가격을 redis에 저장함
    """
    await redis_service.update_stock(redis_db, req.stock_name, new_stock_price)

    return {"msg": "매수요청 완료"}


@router.post("/sell")
async def sell_order(
    req: stock_to_buy_and_sell,
    db=Depends(get_db_session),
    # authorization: str = Header(None),
    redis_db=Depends(get_redis),
    trade_service: TradeService = Depends(),
    redis_service: RedisService = Depends(),
):
    """토큰인증"""

    # if not authorization:
    #     raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")
    # token = authorization.split(" ")[1]  # "Bearer <토큰>"에서 토큰만 추출
    # table에 해당 토큰이 있는지 확인
    token = ""
    if not (login_id := await redis_db.get(token)):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    # 토큰 인증 끝

    """
    주식 있는지 확인 / 주식 없으면 매도 불가능
    """
    user = db.exec(select(User).where(User.login_id == login_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    seller_stock = db.exec(
        select(MyStocks).where(
            MyStocks.login_id == login_id, MyStocks.stock_name == req.stock_name
        )
    ).first()
    if not seller_stock:
        raise HTTPException(status_code=404, detail="보유주식을 찾을 수 없습니다.")

    if seller_stock.quantity < req.quantity:
        raise HTTPException(status_code=400, detail="보유주식이 부족합니다.")

    """
    buy_req 올라온거 trade_stocks에서 찾고, 찾는 수량보다 적게 있으면.. 있는 만큼 판매하고, 없는 만큼 sell_req 를 tradestocks에 올린다
    """
    trade_info = db.exec(
        select(TradeStocks).where(TradeStocks.stock_name == req.stock_name)
    ).first()
    transaction_occurred = False
    buyer = None
    if trade_info:
        if trade_info.is_buy:  # 매수 요청이 존재할 때 거래 처리
            buyer = db.exec(
                select(User).where(User.login_id == trade_info.login_id)
            ).first()
            if trade_info.quantity > req.quantity:
                available_quantity = req.quantity
                trade_info.quantity -= req.quantity
                transaction_occurred = True
            elif trade_info.quantity == req.quantity:
                available_quantity = req.quantity
                db.delete(trade_info)
                transaction_occurred = True
            else:
                available_quantity = trade_info.quantity
                trade_info.quantity = req.quantity - trade_info.quantity
                trade_info.is_buy = False
                trade_info.login_id = login_id
                transaction_occurred = True
        else:  # 기존 매도 요청이 있으면 수량 추가
            if trade_info.login_id == login_id:
                trade_info.quantity += req.quantity
            else:
                trade_info = TradeStocks(
                    login_id=login_id,
                    stock_name=req.stock_name,
                    is_buy=False,
                    quantity=req.quantity,
                )
                db.add(trade_info)
    else:
        # trade_info가 없으면 새로운 매도 요청 추가
        trade_info = TradeStocks(
            login_id=login_id,
            stock_name=req.stock_name,
            is_buy=False,
            quantity=req.quantity,
        )
        db.add(trade_info)

    db.commit()

    """
    tradestocks 에 is_buy 인것과 quantity 를 불러온걸 활용해서 가격변동
    """
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
    db.commit()

    """
    변동된 가격을 redis에 저장함
    """
    redis_service.update_stock(redis_db, req.stock_name, new_stock_price)

    """
    구매한 user balance 차감, Mystocks 에 보유주식 감소
    판매한 user balance 증가, Mystocks 에 보유주식 추가
    """

    if transaction_occurred and buyer:
        buyer.balance -= available_quantity * req.stock_price
        user.balance += available_quantity * req.stock_price

        # 구매자 보유 주식 업데이트
        buyer_stock = db.exec(
            select(MyStocks).where(
                MyStocks.login_id == buyer.login_id,
                MyStocks.stock_name == req.stock_name,
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

        # 판매자 보유 주식 업데이트
        seller_stock.quantity -= available_quantity

    db.commit()
    return {"msg": "매도요청 완료"}
