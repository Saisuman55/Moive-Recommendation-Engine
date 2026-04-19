# Product Requirements Document — Movie Recommendation Engine

## Goals

- Let users register and sign in securely.
- Let users browse movies and submit numeric ratings (0.5–5.0).
- Train a collaborative filtering model (SVD) on pooled ratings and surface personalized top-N recommendations.
- Persist users, movies, ratings, and recommendation rows in PostgreSQL for demos and evaluation.

## Target users

- Students and panel reviewers evaluating an AIML minor project.
- End users who want quick, account-based movie suggestions after rating a handful of titles.

## User stories

1. As a user, I can create an account and log in so my ratings and recommendations are private to my session.
2. As a user, I can see a catalog of movies and enter a rating so the system learns my taste.
3. As a user, I can trigger model training after enough ratings exist so recommendations stay current.
4. As a user, I can view a ranked list of recommended movies with scores after training.

## Feature list

| ID | Feature | Priority |
|----|---------|----------|
| F1 | Email + password auth (JWT), password hashing | P0 |
| F2 | Movie catalog API + seed data for demos | P0 |
| F3 | Create/update per-user ratings | P0 |
| F4 | Train Surprise SVD; persist `.pkl`; write `recommendations` rows | P0 |
| F5 | Read top-N recommendations for the logged-in user | P0 |
| F6 | React UI: auth, list movies, rate, train, show recs | P0 |
| F7 | Docker Compose: Postgres 16, API, web dev | P1 |
| F8 | Alembic migrations for schema | P0 |
| F9 | Optional: OAuth (Google/GitHub) via dedicated auth service | P2 |

## Success metrics

- Cold demo path under 5 minutes: register → rate ≥5 titles (global pool) → train → see top 10 recs.
- API health check and OpenAPI docs available for panel Q&A.
- No secrets or `*.pkl` committed to version control.

## Out of scope (v1)

- Production OAuth wiring for Better Auth Node service (env names reserved for parity).
- Full MovieLens-scale ingestion (can be added later).
