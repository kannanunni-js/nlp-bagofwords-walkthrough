from fastapi import FastAPI,APIRouter
from .io import api_router
from .io import websocket_router

main_router = APIRouter(prefix="/v1",tags=["V1"])
main_router.include_router(api_router)
main_router.include_router(websocket_router)


def setup_api(app:FastAPI):
    app.include_router(main_router)