import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.config import EnvironmentOption, settings
from core.contextmanager import lifespan
from core.middlewares import custom_exception_handler
from core.router import get_global_router

logger = logging.getLogger(__name__)


def create_fastapi_app() -> FastAPI:

    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        port=8000,
        reload=True if settings.ENVIRONMENT != EnvironmentOption.PRODUCTION else False,
        workers=1,
        lifespan=lifespan,
    )

    # Cors conf
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(HTTPException, custom_exception_handler)

    logger.info("Loading routes...")
    app.include_router(get_global_router())

    # Health check endpoint
    @app.get("/health")
    def health_check():
        return {"status": "ok", "environment": settings.ENVIRONMENT.value}

    return app
