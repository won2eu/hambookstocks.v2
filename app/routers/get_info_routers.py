from fastapi import APIRouter, Depends, HTTPException, Header
from app.dependencies.redis_db import get_redis
from app.dependencies.db import get_db_session
from app.models.DB_trade_models import TradeStocks
from app.models.parameter_models import TradeStocksResp, TradeStockReq
from sqlmodel import select

router = APIRouter(prefix="/get_info")


@router.get("/trade_stocks", response_model=TradeStocksResp)
async def get_mypage(
    req: TradeStockReq,
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
    db=Depends(get_db_session),
) -> TradeStocksResp:
    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, deatil="토큰이 필요합니다.")
    # 토큰 검사

    login_id = await redis_db.get(token)
    if not login_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    # TradeStocks 에서 row 전부 불러오기
    trade_info_list = db.exec(
        select(TradeStocks).where(TradeStocks.stock_name == req.stock_name)
    ).all()

    if not trade_info_list:
        return TradeStocksResp(stock_quantity=0, is_buy=None)

    # 서로 다른 login_id 들의 quantity 를 전부 다 합치기
    total_quantity = sum(trade.quantity for trade in trade_info_list)
    is_buy_value = trade_info_list[0].is_buy

    return TradeStocksResp(stock_quantity=total_quantity, is_buy=is_buy_value)
