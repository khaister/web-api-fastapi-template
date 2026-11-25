from fastapi import APIRouter, Depends

from api.deps import require_api_key
from api.v1 import tv_show_view, widget_view

# every v1 route requires an API key
router = APIRouter(prefix="/api/v1", dependencies=[Depends(require_api_key)])
router.include_router(widget_view.router)
router.include_router(tv_show_view.router)
