import httpx

from core.clients.sample_api.futurama_dtos import Info
from web_api.config import get_settings


class FuturamaClient:
    async def get_show_info(self) -> Info | None:
        async with httpx.AsyncClient(base_url=get_settings().sample_api_base_url, timeout=10.0) as client:
            resp = await client.get("/futurama/info")
            resp.raise_for_status()
            data = resp.json()
        return Info(**data[0]) if data else None
