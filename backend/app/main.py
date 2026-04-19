from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.config import get_settings
from app.db import SessionLocal
from app.models import Movie
from app.routers import auth, movies, ratings, recommendations


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    if settings.database_url.startswith("sqlite"):
        from app.db import engine
        from app.models import Base

        Base.metadata.create_all(bind=engine)
    _seed_sample_movies()
    yield


def _seed_sample_movies() -> None:
    samples = [
        ("The Matrix", 1999, "Action, Sci-Fi"),
        ("Inception", 2010, "Action, Sci-Fi, Thriller"),
        ("Interstellar", 2014, "Adventure, Drama, Sci-Fi"),
        ("Spirited Away", 2001, "Animation, Adventure, Family"),
        ("Parasite", 2019, "Comedy, Drama, Thriller"),
        ("The Dark Knight", 2008, "Action, Crime, Drama"),
        ("Pulp Fiction", 1994, "Crime, Drama"),
        ("Forrest Gump", 1994, "Drama, Romance"),
        ("The Shawshank Redemption", 1994, "Drama"),
        ("Whiplash", 2014, "Drama, Music"),
    ]
    db = SessionLocal()
    try:
        if db.execute(select(Movie.id).limit(1)).first() is not None:
            return
        for title, year, genres in samples:
            db.add(Movie(title=title, year=year, genres=genres))
        db.commit()
    finally:
        db.close()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Movie Recommendation Engine", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|192\.168\.\d{1,3}\.\d{1,3})(:\d+)?$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth.router)
    app.include_router(movies.router)
    app.include_router(ratings.router)
    app.include_router(recommendations.router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
