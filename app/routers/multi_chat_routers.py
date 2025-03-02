from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Header,
    HTTPException,
    Depends,
)
import asyncio
from app.services.chatting_service import *
from app.services.redis_service import *
from app.dependencies.redis_db import *
from app.dependencies.jwt_utils import *

router = APIRouter(prefix="/multichat")

manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    authorization: str = Header(None),
    guest_id: str = Header(None),
    redis_db=Depends(get_redis),
):

    token = authorization.split(" ")[1]  # "Bearer <토큰>"에서 토큰만 추출
    guest_id = guest_id

    if login_id := redis_db.get(token):  # 로그인이 되어 있다면..
        await manager.connect(websocket)

        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(f"Client #{login_id} says: {data}")

        except WebSocketDisconnect:
            manager.disconnect(websocket)

    else:  # 로그인이 되어 있지 않다면 ..
        await manager.connect(websocket)

        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(f"Client #{guest_id} says: {data}")

        except WebSocketDisconnect:
            manager.disconnect(websocket)
