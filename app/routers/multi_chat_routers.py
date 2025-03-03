from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    Header,
)
from app.services.multi_chat_service import ConnectionManager
from app.dependencies.redis_db import get_redis

router = APIRouter(prefix="/multichat")

manager = ConnectionManager()

# async def chatting(id, websocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(f"Client #{id} says: {data}")
#     except WebSocketDisconnect:
#             manager.disconnect(websocket)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    authorization: str = Header(None),
    guest_id: str = Header(None),
    redis_db=Depends(get_redis),
):

    token = authorization.split(" ")[1]  # "Bearer <토큰>"에서 토큰만 추출
    guest_id = guest_id  # Front 에서 형식 맞춰줘야함

    if login_id := await redis_db.get(token):
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(f"Client #{login_id} says: {data}")

        except WebSocketDisconnect:
            manager.disconnect(websocket)

    else:
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(f"Client #{guest_id} says: {data}")

        except WebSocketDisconnect:
            manager.disconnect(websocket)
