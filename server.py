from fastapi import FastAPI, WebSocket
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates


app = FastAPI(title='Example')
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print('Accepting client connection...')
    count = 1
    while True:
        try:
            data = await websocket.receive_json()
            data.update({"Number": str(count)})
            await websocket.send_json(data)
            count += 1
        except Exception as e:
            print('error:', e)
            break
    print('Bye')
