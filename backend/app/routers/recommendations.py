from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Movie, User
from app.services import recommender

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/train")
def train(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> dict:
    return recommender.train_and_persist(db)


@router.get("")
def list_recommendations(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    limit: int = Query(10, ge=1, le=50),
) -> list[dict]:
    pairs = recommender.top_for_user(db, user.id, limit=limit)
    if not pairs:
        return []
    ids = [p[0] for p in pairs]
    rows = db.execute(select(Movie).where(Movie.id.in_(ids))).scalars().all()
    movies = {m.id: m for m in rows}
    out = []
    for mid, score in pairs:
        m = movies.get(mid)
        if m:
            out.append(
                {
                    "movie_id": m.id,
                    "title": m.title,
                    "year": m.year,
                    "genres": m.genres,
                    "score": score,
                }
            )
    return out
