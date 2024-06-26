from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import os
import aioredis

app = FastAPI()

# Configurar a pasta static para servir arquivos estáticos
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Gerenciar conexões WebSocket ativas
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# Endpoint para servir a página HTML do chat
@app.get("/")
async def get():
    html_path = os.path.join(static_dir, "index.html")
    with open(html_path) as f:
        return HTMLResponse(content=f.read(), status_code=200)


# Endpoint WebSocket para receber e distribuir mensagens
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Client left the chat")


# Configuração para conectar ao Redis
async def startup():
    app.redis = await aioredis.from_url("redis://redis", encoding="utf-8")


async def shutdown():
    app.redis.close()
    await app.redis.wait_closed()


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
