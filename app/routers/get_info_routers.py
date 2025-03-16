from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)
import asyncio
from app.dependencies.redis_db import get_redis


router = APIRouter(prefix="/get_info")

redis = None


@router.on_event("startup")
async def startup():
    global redis
    redis = await get_redis()


@router.on_event("shutdown")
async def shutdown():
    await redis.close()


@router.websocket("/stock_info")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            stock_data = await redis.hgetall("stocks")  # ✅ Redis 연결 유지
            await websocket.send_json(stock_data)
            await asyncio.sleep(1)  # 1초마다 업데이트
    except WebSocketDisconnect:
        print("WebSocket 연결이 종료되었습니다.")
