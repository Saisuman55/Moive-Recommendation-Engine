from pydantic import BaseModel, Field


class RatingCreate(BaseModel):
    movie_id: int
    rating: float = Field(ge=0.5, le=5.0)


class RatingRead(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: float

    model_config = {"from_attributes": True}
