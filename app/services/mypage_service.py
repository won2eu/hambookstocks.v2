import logging
from sqlmodel import Session, select, delete
from fastapi import HTTPException
from app.models.DB_user_models import User
from app.models.DB_mystocks_models import MyStocks
from app.models.DB_trade_models import TradeStocks
from app.models.DB_User_stocks_models import UserStocks


class AccountService:
    def __init__(self, db: Session):
        self.db = db

    def delete_account(self, login_id: str):

        # 사용자 정보 삭제
        user = self.db.exec(select(User).where(User.login_id == login_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        self.db.delete(user)

        # 사용자가 보유한 주식 정보 삭제
        self._delete_user_owned_stocks(login_id)

        # 사용자의 거래 요청 삭제
        self._delete_user_trades(login_id)

        # 사용자가 상장한 주식 삭제
        self._delete_user_stocks(login_id)

        self.db.commit()
        logging.info(f"User {login_id}'s info has been deleted successfully")

    """사용자가 보유한 주식 삭제"""

    def _delete_user_owned_stocks(self, login_id: str):
        user_own_stocks = self.db.exec(
            select(MyStocks).where(MyStocks.login_id == login_id)
        ).all()
        for stock in user_own_stocks:
            self.db.delete(stock)

    """사용자의 거래 요청 삭제"""

    def _delete_user_trades(self, login_id: str):
        user_trades = self.db.exec(
            select(TradeStocks).where(TradeStocks.login_id == login_id)
        ).all()
        for trade in user_trades:
            self.db.delete(trade)

    """사용자가 상장한 주식 삭제"""

    def _delete_user_stocks(self, login_id: str):
        user_stocks = self.db.exec(
            select(UserStocks).where(UserStocks.login_id == login_id)
        ).all()
        for stock in user_stocks:
            self.db.delete(stock)

    """탈퇴한 사용자가 상장한 주식을 가지고 있는 사람들 주식 삭제"""

    def delete_victim_stock(self, login_id: str):
        user_stocks = self.db.exec(
            select(UserStocks).where(UserStocks.login_id == login_id)
        ).all()
        stock_names = [stock.stock_name for stock in user_stocks]

        if not stock_names:
            logging.info("삭제할 주식이 없습니다.")
            return

        self.db.exec(delete(MyStocks).where(MyStocks.stock_name.in_(stock_names)))
        self.db.commit()

        logging.info(f"User {login_id}'s stocks have been deleted successfully")
