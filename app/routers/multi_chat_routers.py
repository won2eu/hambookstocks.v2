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
    redis_db=Depends(get_redis),
):

    await websocket.accept()
    print("WebSocket 연결 수락됨")
    auth_data = await websocket.receive_json()
    token = None
    guest_id = None

    if auth_data["type"] == "auth":
        if "authorization" in auth_data:
            token = auth_data["authorization"].split(" ")[1]
        if "guest_id" in auth_data:
            guest_id = auth_data["guest_id"]

    if token and (login_id := await redis_db.get(token)):  # 로그인이 되어 있다면..
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
