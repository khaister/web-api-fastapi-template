import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1 import router as v1_router
from common_libs.logging import ColorHandler
from core.db import create_tables, dispose_engine
from web_api.config import get_settings


def _configure_logging() -> None:
    settings = get_settings()
    handler: logging.Handler = ColorHandler() if settings.is_local else logging.StreamHandler()
    logging.basicConfig(level=settings.log_level.upper(), handlers=[handler], force=True)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    _configure_logging()
    await create_tables()
    yield
    await dispose_engine()


def create_app() -> FastAPI:
    app = FastAPI(title="Web API", version="0.1.0", lifespan=lifespan)
    app.include_router(v1_router)

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
