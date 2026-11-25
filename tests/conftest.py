from collections.abc import AsyncIterator

import httpx
import pytest

from core.db import dispose_engine
from web_api.config import get_settings
from web_api.main import create_app

API_KEY = "test-api-key"


@pytest.fixture
async def client(tmp_path, monkeypatch) -> AsyncIterator[httpx.AsyncClient]:
    """An async client wired to a fresh app with an isolated sqlite database."""
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("API_KEY", API_KEY)
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{tmp_path / 'test.db'}")
    get_settings.cache_clear()
    await dispose_engine()

    app = create_app()
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
            yield c

    get_settings.cache_clear()


@pytest.fixture
def auth() -> dict[str, str]:
    return {"X-API-Key": API_KEY}
