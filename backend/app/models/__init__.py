from app.models.base import Base
from app.models.movie import Movie
from app.models.rating import Rating
from app.models.recommendation import Recommendation
from app.models.user import User

__all__ = ["Base", "User", "Movie", "Rating", "Recommendation"]
