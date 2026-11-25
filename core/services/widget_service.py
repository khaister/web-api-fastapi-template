from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dtos.widget_dtos import WidgetCreate, WidgetUpdate
from core.models import Widget


async def list_widgets(session: AsyncSession) -> list[Widget]:
    result = await session.scalars(select(Widget).order_by(Widget.created_on.desc(), Widget.id.desc()))
    return list(result)


async def get_widget(session: AsyncSession, widget_id: int) -> Widget | None:
    return await session.get(Widget, widget_id)


async def create_widget(session: AsyncSession, data: WidgetCreate) -> Widget:
    widget = Widget(**data.model_dump())
    session.add(widget)
    await session.commit()
    await session.refresh(widget)
    return widget


async def update_widget(session: AsyncSession, widget: Widget, data: WidgetUpdate) -> Widget:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(widget, field, value)
    await session.commit()
    await session.refresh(widget)
    return widget


async def delete_widget(session: AsyncSession, widget: Widget) -> None:
    await session.delete(widget)
    await session.commit()
