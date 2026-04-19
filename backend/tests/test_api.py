from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_movies_seeded(client: TestClient) -> None:
    r = client.get("/movies?limit=20")
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 1
    assert "title" in data[0]


def test_register_login_me_flow(client: TestClient) -> None:
    r = client.post(
        "/auth/register",
        json={"email": "pytest_user@example.com", "password": "testpass12"},
    )
    assert r.status_code == 201
    uid = r.json()["id"]

    r = client.post(
        "/auth/login",
        json={"email": "pytest_user@example.com", "password": "testpass12"},
    )
    assert r.status_code == 200
    token = r.json()["access_token"]

    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "pytest_user@example.com"
    assert r.json()["id"] == uid


def test_ratings_and_train_skip_with_few_ratings(client: TestClient) -> None:
    client.post(
        "/auth/register",
        json={"email": "rater@example.com", "password": "testpass12"},
    )
    r = client.post(
        "/auth/login",
        json={"email": "rater@example.com", "password": "testpass12"},
    )
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    movies = client.get("/movies?limit=5").json()
    assert len(movies) >= 2
    mid0, mid1 = movies[0]["id"], movies[1]["id"]

    assert client.post("/ratings", headers=headers, json={"movie_id": mid0, "rating": 4.0}).status_code == 201
    assert client.post("/ratings", headers=headers, json={"movie_id": mid1, "rating": 3.0}).status_code == 201

    r = client.post("/recommendations/train", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "skipped"

    r = client.get("/recommendations?limit=5", headers=headers)
    assert r.status_code == 200
    assert r.json() == []


def test_train_ok_with_enough_ratings(client: TestClient) -> None:
    """Needs ≥5 global ratings; seeds + prior tests may already satisfy — add explicit ratings."""
    client.post(
        "/auth/register",
        json={"email": "bulk@example.com", "password": "testpass12"},
    )
    r = client.post(
        "/auth/login",
        json={"email": "bulk@example.com", "password": "testpass12"},
    )
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    movies = client.get("/movies?limit=10").json()
    for i, m in enumerate(movies):
        code = client.post(
            "/ratings",
            headers=headers,
            json={"movie_id": m["id"], "rating": 2.5 + (i % 3)},
        ).status_code
        assert code in (200, 201)

    r = client.post("/recommendations/train", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["ratings_used"] >= 5

    r = client.get("/recommendations?limit=5", headers=headers)
    assert r.status_code == 200
    recs = r.json()
    assert len(recs) >= 1
    assert "score" in recs[0]
