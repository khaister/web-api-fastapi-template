from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WidgetCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str
    quantity: int = Field(ge=0)
    active: bool = True


class WidgetUpdate(BaseModel):
    """Partial update: only the fields that are sent are changed."""

    name: str | None = Field(default=None, max_length=100)
    description: str | None = None
    quantity: int | None = Field(default=None, ge=0)
    active: bool | None = None


class WidgetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    quantity: int
    active: bool
    created_on: datetime
    updated_on: datetime
