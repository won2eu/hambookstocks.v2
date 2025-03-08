from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.DB_user_models import User
from app.models.DB_mystocks_models import MyStocks
from app.models.DB_trade_models import TradeStocks
from app.models.DB_User_stocks_models import UserStocks


def delete_account(login_id: str, db: Session):

    # 사용자 정보 삭제
    user = db.exec(select(User).where(User.login_id == login_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 사용자가 보유한 주식 정보 삭제
    user_own_stocks = db.exec(
        select(MyStocks).where(MyStocks.login_id == login_id)
    ).all()
    for own_stock in user_own_stocks:
        db.delete(own_stock)

    # 사용자의 거래 요청들들 삭제
    user_trades = db.exec(
        select(TradeStocks).where(TradeStocks.login_id == login_id)
    ).all()
    for user_trade in user_trades:
        db.delete(user_trade)
    # 사용자가 상장한 주식들 삭제제
    user_stocks = db.exec(
        select(UserStocks).where(UserStocks.login_id == login_id)
    ).all()
    for user_stock in user_stocks:
        db.delete(user_stock)

    db.commit()
