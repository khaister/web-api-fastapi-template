from fastapi import APIRouter

from core.dtos.tv_show_dtos import TvShows
from core.services import tv_show_service

router = APIRouter(prefix="/tv-shows", tags=["tv-shows"])


@router.get("", response_model=TvShows)
async def list_shows() -> TvShows:
    return await tv_show_service.get_shows()
