from pydantic import BaseModel, Field


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=512)
    year: int | None = Field(default=None, ge=1888, le=2100)
    genres: str | None = None


class MovieRead(BaseModel):
    id: int
    title: str
    year: int | None
    genres: str | None

    model_config = {"from_attributes": True}
