from typing import List

from fastapi import FastAPI, WebSocket
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates


app = FastAPI(title='Example')
templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await manager.connect(websocket)
    count = 1
    while True:
        try:
            data = await websocket.receive_json()
            data.update({"Number": str(count)})
            await manager.broadcast(data)
            count += 1
        except Exception as e:
            print('error:', e)
            break
    print('Bye')
