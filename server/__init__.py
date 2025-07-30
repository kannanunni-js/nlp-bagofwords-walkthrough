from fastapi import FastAPI, status
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from inference import setup_api
from core.events import event_manager, settings


def create_app():
    """
    Creates a FastAPI app with all the necessary routes and exception handlers.

    Returns:
        app: A FastAPI app with all the necessary routes and exception handlers.
    """
    _app = FastAPI(
        debug=settings.DEBUG == "on",
        title=settings.PROJECT_NAME,
        description=f"WELCOME TO {settings.PROJECT_NAME}",
        version=settings.PROJECT_VERSION,
        docs_url="/",
        redoc_url=None,
        openapi_tags=[],

        lifespan=event_manager,

        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ]
    )
    setup_api(_app)

    return _app

app = create_app()
