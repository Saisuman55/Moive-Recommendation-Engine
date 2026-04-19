import os
import pickle
from pathlib import Path

import pandas as pd
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from surprise import Dataset, Reader, SVD

from app.config import get_settings
from app.models import Movie, Rating, Recommendation


def _model_path() -> str:
    path = get_settings().model_path
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    return path


def train_and_persist(db: Session, n_factors: int = 20, n_epochs: int = 20) -> dict:
    rows = db.execute(
        select(Rating.user_id, Rating.movie_id, Rating.rating)
    ).all()
    if len(rows) < 5:
        return {"status": "skipped", "reason": "Need at least 5 ratings to train."}

    df = pd.DataFrame(rows, columns=["user_id", "movie_id", "rating"])
    df["user_id"] = df["user_id"].astype(str)
    df["movie_id"] = df["movie_id"].astype(str)

    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(df[["user_id", "movie_id", "rating"]], reader)
    trainset = data.build_full_trainset()
    algo = SVD(n_factors=n_factors, n_epochs=n_epochs, random_state=42)
    algo.fit(trainset)

    path = _model_path()
    with open(path, "wb") as f:
        pickle.dump(algo, f)

    db.execute(delete(Recommendation))
    db.flush()
    user_ids = df["user_id"].unique().tolist()
    movie_ids_all = (
        db.execute(select(Movie.id)).scalars().all()
    )
    movie_ids_set = {str(mid) for mid in movie_ids_all}
    version = "svd-v1"

    for uid in user_ids:
        rated = set(df.loc[df["user_id"] == uid, "movie_id"].astype(str))
        candidates = [m for m in movie_ids_set if m not in rated]
        if not candidates:
            continue
        scores: list[tuple[str, float]] = []
        for mid in candidates[:400]:
            est = algo.predict(uid, mid).est
            scores.append((mid, float(est)))
        scores.sort(key=lambda x: x[1], reverse=True)
        for mid, score in scores[:25]:
            db.add(
                Recommendation(
                    user_id=int(uid),
                    movie_id=int(mid),
                    score=score,
                    model_version=version,
                )
            )
    db.commit()
    return {"status": "ok", "ratings_used": len(rows), "model_path": path}


def model_loaded() -> bool:
    return os.path.isfile(_model_path())


def load_algo() -> SVD:
    with open(_model_path(), "rb") as f:
        return pickle.load(f)


def top_for_user(db: Session, user_id: int, limit: int = 10) -> list[tuple[int, float]]:
    rows = db.execute(
        select(Recommendation.movie_id, Recommendation.score)
        .where(Recommendation.user_id == user_id)
        .order_by(Recommendation.score.desc())
        .limit(limit)
    ).all()
    return [(int(r[0]), float(r[1])) for r in rows]
