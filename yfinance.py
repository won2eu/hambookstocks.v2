from fastapi import FastAPI, HTTPException
import yfinance as yf

app = FastAPI()

@app.get('/info/name/{name}')
async def get_stock_info(name: str):
    try:
        # 주식 티커를 사용하여 주식 데이터 가져오기
        stock = yf.Ticker(name)
        stock_info = stock.info
        
        # 주식 정보 반환
        return {
            "symbol": stock_info.get("symbol"),
            "name": stock_info.get("shortName"),
            "price": stock_info.get("currentPrice"),
            "market_cap": stock_info.get("marketCap"),
            "previous_close": stock_info.get("previousClose"),
            "day_high": stock_info.get("dayHigh"),
            "day_low": stock_info.get("dayLow"),
        }
    except Exception as e:
        # 오류가 발생한 경우
        raise HTTPException(status_code=404, detail=f"Stock {name} not found: {str(e)}")
