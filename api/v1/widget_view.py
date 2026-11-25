from fastapi import APIRouter, HTTPException, Response, status

from api.deps import SessionDep
from core.dtos.widget_dtos import WidgetCreate, WidgetRead, WidgetUpdate
from core.models import Widget
from core.services import widget_service

router = APIRouter(prefix="/widgets", tags=["widgets"])


async def _get_or_404(session: SessionDep, widget_id: int) -> Widget:
    widget = await widget_service.get_widget(session, widget_id)
    if widget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    return widget


@router.get("", response_model=list[WidgetRead])
async def list_widgets(session: SessionDep):
    return await widget_service.list_widgets(session)


@router.post("", response_model=WidgetRead, status_code=status.HTTP_201_CREATED)
async def create_widget(data: WidgetCreate, session: SessionDep):
    return await widget_service.create_widget(session, data)


@router.get("/{widget_id}", response_model=WidgetRead)
async def get_widget(widget_id: int, session: SessionDep):
    return await _get_or_404(session, widget_id)


@router.patch("/{widget_id}", response_model=WidgetRead)
async def update_widget(widget_id: int, data: WidgetUpdate, session: SessionDep):
    widget = await _get_or_404(session, widget_id)
    return await widget_service.update_widget(session, widget, data)


@router.delete("/{widget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_widget(widget_id: int, session: SessionDep) -> Response:
    widget = await _get_or_404(session, widget_id)
    await widget_service.delete_widget(session, widget)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
