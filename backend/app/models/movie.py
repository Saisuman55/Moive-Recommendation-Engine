from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(512), index=True)
    year: Mapped[int | None] = mapped_column(nullable=True)
    genres: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    ratings: Mapped[list["Rating"]] = relationship(back_populates="movie")
    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="movie"
    )
