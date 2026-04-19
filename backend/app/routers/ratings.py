from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Movie, Rating, User
from app.schemas.rating import RatingCreate, RatingRead

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post("", response_model=RatingRead, status_code=status.HTTP_201_CREATED)
def create_rating(
    body: RatingCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Rating:
    if db.get(Movie, body.movie_id) is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    existing = db.scalars(
        select(Rating).where(
            Rating.user_id == user.id,
            Rating.movie_id == body.movie_id,
        )
    ).first()
    if existing:
        existing.rating = body.rating
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    r = Rating(user_id=user.id, movie_id=body.movie_id, rating=body.rating)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.get("/me", response_model=list[RatingRead])
def my_ratings(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[Rating]:
    rows = db.execute(select(Rating).where(Rating.user_id == user.id)).scalars().all()
    return list(rows)
