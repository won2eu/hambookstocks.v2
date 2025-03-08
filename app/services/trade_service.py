from sqlmodel import select
from app.dependencies.db import get_db_session
from app.models.DB_Market_stocks_models import MarketStocks
from app.models.DB_User_stocks_models import UserStocks


class trade_service:
    def update_price(self, db, stock):
        alpha = 1
        stock.stock_price += (stock.trend_buy - stock.trend_sell) * alpha

        db.commit()
        db.refresh(stock)

        # 새로운 가격으로 업데이트하기

    def update_sell(self, db, stock, quantity):
        stock.trend_sell += quantity
        stock.total_sell += quantity

        db.commit()
        db.refresh(stock)

    def update_buy(self, db, stock, quantity):
        stock.trend_buy += quantity
        stock.total_buy += quantity

        db.commit()
        db.refresh(stock)


def clear_trend():
    db = next(get_db_session())
    market_stocks = db.exec(select(MarketStocks)).all()
    user_stocks = db.exec(select(UserStocks)).all()

    for stock in market_stocks:
        stock.trend_sell = 0
        stock.trend_buy = 0

    for stock in user_stocks:
        stock.trend_sell = 0
        stock.trend_buy = 0

    db.commit()
