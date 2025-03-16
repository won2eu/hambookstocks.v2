from fastapi import APIRouter, Depends, HTTPException, Header
from app.dependencies.redis_db import get_redis
from app.dependencies.db import get_db_session
from app.models.DB_trade_models import TradeStocks
from app.models.parameter_models import TradeStocksResp
from app.services.auth_service import AuthService
from sqlmodel import select
from typing import List

router = APIRouter(prefix="/get_info")


@router.get("/trade_stocks", response_model=List[TradeStocksResp])
async def get_mypage(
    authorization: str = Header(None),
    redis_db=Depends(get_redis),
    db=Depends(get_db_session),
) -> list:
    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, deatil="토큰이 필요합니다.")
    # 토큰 검사

    login_id = await redis_db.get(token)
    if not login_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    # TradeStocks 에서 column 전부 불러오기
    trade_info_list = db.exec(select(TradeStocks)).all()

    trade_info_resp_list = [
        TradeStocksResp(
            stock_name=trade.stock_name,
            stock_quantity=trade.quantity,
            is_buy=trade.is_buy,
        )
        for trade in trade_info_list
    ]

    return trade_info_resp_list
