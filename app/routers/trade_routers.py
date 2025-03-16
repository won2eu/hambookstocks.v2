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
from app.services.redis_service import RedisService
from sqlmodel import select

router = APIRouter(prefix="/trade")

# 주식 가격변동계수
alpha = 0.1


@router.post("/buy_request")  # req: 수량, 금액, 주식 코드,
async def buy_stock(
    req: stock_to_buy_and_sell,
    db: Session = Depends(get_db_session),
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
    redis_service: RedisService = Depends(),
):
    if not authorization:
        raise HTTPException(status_code=401, detail="로그인하셔야 합니다.")

    token = authorization.split(" ")[1]

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
    trade_info_list = db.exec(
        select(TradeStocks).where(TradeStocks.stock_name == req.stock_name)
    ).all()
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
            remaining_quantity = req.quantity  # 사용자가 구매하고자 하는 남은 수량
            transaction_occurred = False  # 거래 발생 여부
            trade_transactions = []  # 거래 내역을 저장할 리스트

            for (
                trade_info
            ) in trade_info_list:  # 여러 개의 판매 주문을 처리할 수 있도록 반복문 사용
                if trade_info.quantity > remaining_quantity:
                    trade_amount = remaining_quantity  # 요청 수량만큼 거래 가능
                    trade_info.quantity -= (
                        remaining_quantity  # 판매 주문에서 해당 수량 차감
                    )
                    transaction_occurred = True
                    trade_transactions.append(
                        (trade_info.login_id, trade_amount)
                    )  # 거래 정보 저장
                    break  # 요청한 수량을 전부 처리했으므로 종료

                elif trade_info.quantity == remaining_quantity:
                    trade_amount = remaining_quantity  # 요청 수량만큼 거래 가능
                    db.delete(trade_info)  # 판매 주문을 전부 처리했으므로 삭제
                    transaction_occurred = True
                    trade_transactions.append(
                        (trade_info.login_id, trade_amount)
                    )  # 거래 정보 저장
                    break  # 요청한 수량을 전부 처리했으므로 종료

                else:  # trade_info.quantity < remaining_quantity
                    trade_amount = trade_info.quantity  # 판매 주문의 모든 수량을 사용
                    remaining_quantity -= trade_info.quantity  # 남은 요청 수량 업데이트
                    db.delete(trade_info)  # 판매 주문 소진으로 삭제
                    transaction_occurred = True
                    trade_transactions.append(
                        (trade_info.login_id, trade_amount)
                    )  # 거래 정보 저장

            # 요청한 수량이 판매 주문을 모두 소진하고도 남아있는 경우
            if remaining_quantity > 0:
                new_trade_info = TradeStocks(
                    quantity=remaining_quantity,
                    stock_name=req.stock_name,
                    is_buy=True,
                    login_id=login_id,
                )
                db.add(new_trade_info)  # 새로운 구매 요청 등록
    else:
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
    if transaction_occurred and trade_transactions:
        user.balance -= sum(
            trade_amount * req.stock_price for _, trade_amount in trade_transactions
        )  # 구매자 balance 차감

        # 판매자 balance , 주식 수량 감소
        for seller_id, trade_amount in trade_transactions:
            seller = db.exec(select(User).where(User.login_id == seller_id)).first()
            if seller:
                seller.balance += trade_amount * req.stock_price  # 판매자 balance 증가

                # 판매자의 주식 수량 감소
                seller_stock = db.exec(
                    select(MyStocks).where(
                        MyStocks.login_id == seller_id,
                        MyStocks.stock_name == req.stock_name,
                    )
                ).first()

                seller_stock.quantity -= trade_amount

        # 구매자의 보유 주식 업데이트
        buyer_stock = db.exec(
            select(MyStocks).where(
                MyStocks.login_id == login_id, MyStocks.stock_name == req.stock_name
            )
        ).first()
        if not buyer_stock:
            buyer_stock = MyStocks(
                login_id=login_id,
                stock_name=req.stock_name,
                quantity=sum(trade_amount for _, trade_amount in trade_transactions),
            )
            db.add(buyer_stock)
        else:
            buyer_stock.quantity += sum(
                trade_amount for _, trade_amount in trade_transactions
            )

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


@router.post("/sell_request")
async def sell_order(
    req: stock_to_buy_and_sell,
    db=Depends(get_db_session),
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
    redis_service: RedisService = Depends(),
):
    """토큰인증"""

    if not authorization:
        raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")
    token = authorization.split(" ")[1]  # "Bearer <토큰>"에서 토큰만 추출

    if not (login_id := await redis_db.get(token)):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

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
        raise HTTPException(status_code=400, detail="보유주식 수량이이 부족합니다.")

    """
    buy_req 올라온거 trade_stocks에서 찾고, 찾는 수량보다 적게 있으면.. 있는 만큼 판매하고, 없는 만큼 sell_req 를 tradestocks에 올린다
    """
    trade_info = db.exec(
        select(TradeStocks).where(TradeStocks.stock_name == req.stock_name)
    ).first()
    trade_info_list = db.exec(
        select(TradeStocks).where(TradeStocks.stock_name == req.stock_name)
    ).all()
    transaction_occurred = False

    if trade_info:
        # 올라온게 sell 일때
        if not trade_info.is_buy:  # 동일한 판매자가 존재하는 경우
            if trade_info.login_id == login_id:
                # 동일한 login_id인 경우 수량만 업데이트
                trade_info.quantity += req.quantity
            else:
                # 다른 login_id인 경우 새로운 판매 요청 추가
                trade_info = TradeStocks(
                    login_id=login_id,
                    stock_name=req.stock_name,
                    is_buy=False,
                    quantity=req.quantity,
                )
                db.add(trade_info)
        else:
            # 올라온게 buy 일때
            remaining_quantity = req.quantity  # 사용자가 판매하고자 하는 남은 수량
            transaction_occurred = False  # 거래 발생 여부
            trade_transactions = []  # 거래 내역을 저장할 리스트

            for trade_info in trade_info_list:  # 여러 개의 매수 주문을 처리할 수 있도록
                if trade_info.quantity > remaining_quantity:
                    trade_amount = remaining_quantity  # 요청 수량만큼 거래 가능
                    trade_info.quantity -= (
                        remaining_quantity  # 매수 주문에서 해당 수량 차감
                    )
                    transaction_occurred = True
                    trade_transactions.append(
                        (trade_info.login_id, trade_amount)
                    )  # 거래 정보 저장
                    break  # 요청한 수량을 전부 처리했으므로 종료

                elif trade_info.quantity == remaining_quantity:
                    trade_amount = remaining_quantity  # 요청 수량만큼 거래 가능
                    db.delete(trade_info)  # 매수 주문을 전부 처리했으므로 삭제
                    transaction_occurred = True
                    trade_transactions.append(
                        (trade_info.login_id, trade_amount)
                    )  # 거래 정보 저장
                    break  # 요청한 수량을 전부 처리했으므로 종료

                else:  # trade_info.quantity < remaining_quantity
                    trade_amount = trade_info.quantity  # 매수 주문의 모든 수량을 사용
                    remaining_quantity -= trade_info.quantity  # 남은 요청 수량 업데이트
                    db.delete(trade_info)  # 매수 주문 소진으로 삭제
                    transaction_occurred = True
                    trade_transactions.append(
                        (trade_info.login_id, trade_amount)
                    )  # 거래 정보 저장

            # 요청한 수량이 매수 주문을 모두 소진하고도 남아있는 경우
            if remaining_quantity > 0:
                new_trade_info = TradeStocks(
                    quantity=remaining_quantity,
                    stock_name=req.stock_name,
                    is_buy=False,
                    login_id=login_id,
                )
                db.add(new_trade_info)  # 새로운 판매 요청 등록
    else:
        trade_info = TradeStocks(
            login_id=login_id,
            stock_name=req.stock_name,
            is_buy=False,
            quantity=req.quantity,
        )
        db.add(trade_info)

    db.commit()

    """
    구매한 user balance 차감, Mystocks 에 보유주식 추가
    판매한 user balance 증가, Mystocks 에 보유주식 감소
    """
    if transaction_occurred and trade_transactions:
        seller = db.exec(select(User).where(User.login_id == login_id)).first()

        # 판매자 balance 증가
        seller.balance += sum(
            trade_amount * req.stock_price for _, trade_amount in trade_transactions
        )

        # 여러 구매자의 balance 및 MyStocks 업데이트
        for buyer_id, trade_amount in trade_transactions:
            buyer = db.exec(select(User).where(User.login_id == buyer_id)).first()
            if buyer:
                buyer.balance -= trade_amount * req.stock_price  # 구매자 balance 차감

                # 구매자의 보유 주식 업데이트
                buyer_stock = db.exec(
                    select(MyStocks).where(
                        MyStocks.login_id == buyer_id,
                        MyStocks.stock_name == req.stock_name,
                    )
                ).first()

                if not buyer_stock:
                    buyer_stock = MyStocks(
                        login_id=buyer_id,
                        stock_name=req.stock_name,
                        quantity=trade_amount,
                    )
                    db.add(buyer_stock)
                else:
                    buyer_stock.quantity += trade_amount

        # 판매자의 보유 주식 감소
        seller_stock = db.exec(
            select(MyStocks).where(
                MyStocks.login_id == login_id,
                MyStocks.stock_name == req.stock_name,
            )
        ).first()

        if seller_stock:
            seller_stock.quantity -= sum(
                trade_amount for _, trade_amount in trade_transactions
            )

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

    return {"msg": "매도 요청 완료"}
