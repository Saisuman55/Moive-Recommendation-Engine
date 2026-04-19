"""Set env before any `app` import so DB engine uses an isolated SQLite file."""

from __future__ import annotations

import os
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

_fd, _DB_FILE = tempfile.mkstemp(suffix="-pytest.db")
os.close(_fd)
_DB_PATH = Path(_DB_FILE)

os.environ["DATABASE_URL"] = "sqlite:///" + _DB_PATH.resolve().as_posix()
os.environ["BETTER_AUTH_SECRET"] = "test-jwt-secret-key-min-32-chars-long!!"
os.environ["MODEL_PATH"] = str(_DB_PATH.parent / "pytest_svd_model.pkl")

# Drop cached settings so a prior import (if any) does not win.
from app.config import get_settings

get_settings.cache_clear()

from app.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


def pytest_sessionfinish(_session: pytest.Session, exitstatus: int) -> None:
    try:
        _DB_PATH.unlink(missing_ok=True)
    except OSError:
        pass
    pkl = Path(os.environ["MODEL_PATH"])
    try:
        pkl.unlink(missing_ok=True)
    except OSError:
        pass
