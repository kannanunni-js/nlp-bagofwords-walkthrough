from fastapi import WebSocket, WebSocketDisconnect
from . import websocket_router
from loguru import logger

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.success("Welcome to the course! Check out the WebSocket endpoint.")
    await websocket.send_text("Welcome to the course! Check out the WebSocket endpoint.")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        print("Client disconnected")
