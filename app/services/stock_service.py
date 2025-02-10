import yfinance as yf
from app.models.stock_model import StockInfo
from datetime import date, timedelta


def get_today_high_low(symbol: str):
    try:
        ticker = yf.Ticker(symbol)

        # 오늘 날짜
        today = date.today()

        # 오늘 날짜의 데이터 가져오기 (실시간 데이터는 1일 전부터)
        data = ticker.history(period="1d")

        # 데이터가 비어있으면 전날 데이터 가져오기
        if data.empty:
            yesterday = today - timedelta(days=1)
            data = ticker.history(period="1d", start=yesterday, end=today)

        # 오늘 최고가/최저가
        today_high = data['High'][-1]
        today_low = data['Low'][-1]

        return today_high, today_low

    except Exception as e:
        raise Exception(f"Error fetching stock info for {symbol}: {e}")


def get_stock_info(symbol: str) -> StockInfo:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        today_high, today_low = get_today_high_low(symbol)


        current_price = round(info.get("currentPrice"),2)
        today_high = round(today_high,2)
        today_low = round(today_low,2)
        volume = info.get("volume")

        return StockInfo(symbol, current_price, today_high, today_low, volume)

    except Exception as e:
        raise Exception(f"Error fetching stock info for {symbol}: {e}")