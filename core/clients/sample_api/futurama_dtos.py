from pydantic import BaseModel, Field


class Creator(BaseModel):
    name: str
    url: str | None = None


class Info(BaseModel):
    id: int
    synopsis: str | None = None
    years_aired: str | None = Field(default=None, alias="yearsAired")
    creators: list[Creator] = []
