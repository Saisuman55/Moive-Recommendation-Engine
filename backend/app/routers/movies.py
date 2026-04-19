from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Movie
from app.schemas.movie import MovieCreate, MovieRead

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("", response_model=list[MovieRead])
def list_movies(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> list[Movie]:
    rows = db.execute(select(Movie).offset(skip).limit(limit)).scalars().all()
    return list(rows)


@router.post("", response_model=MovieRead, status_code=201)
def create_movie(body: MovieCreate, db: Annotated[Session, Depends(get_db)]) -> Movie:
    m = Movie(title=body.title, year=body.year, genres=body.genres)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.get("/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: int, db: Annotated[Session, Depends(get_db)]) -> Movie:
    m = db.get(Movie, movie_id)
    if m is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return m
