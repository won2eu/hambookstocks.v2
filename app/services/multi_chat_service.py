from fastapi import WebSocket
import asyncio


class ConnectionManager:
    def init(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        await asyncio.gather(
            *[connection.send_text(message) for connection in self.active_connections]
        )
