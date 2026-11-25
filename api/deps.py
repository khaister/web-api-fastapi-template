import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from web_api.config import Settings, get_settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def require_api_key(
    api_key: Annotated[str | None, Security(_api_key_header)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    """Reject the request unless it carries the configured API key. Fails closed when no key is configured."""
    if not settings.api_key or not api_key or not secrets.compare_digest(api_key, settings.api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")
