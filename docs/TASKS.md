# Project task list — Movie Recommendation Engine

Work **top to bottom**. Each task is one clear action with no overlap.

---

## Phase 1 — Docs (complete when files exist)

- [x] **1.1** Create `docs/PRD.md` (goals, users, stories, features, metrics).
- [x] **1.2** Create `docs/DESIGN.md` (colors, layout, typography, screens).
- [x] **1.3** Create `docs/TECHSTACK.md` (FastAPI, React, Surprise, Postgres, Docker, env vars).

Optional: export your existing Word briefs into these files if the course requires exact wording match.

---

## Phase 2 — Build (scaffold + run)

- [x] **2.1** Backend: FastAPI app, SQLAlchemy models (`users`, `movies`, `ratings`, `recommendations`), settings from env.
- [x] **2.2** Backend: JWT auth routes (`/auth/register`, `/auth/login`, `/auth/me`).
- [x] **2.3** Backend: movie + rating + recommendation routes; Surprise SVD train + persist recommendations.
- [x] **2.4** Backend: Alembic migration `001_initial_schema`; Dockerfile runs `alembic upgrade head` then uvicorn.
- [x] **2.5** Frontend: React 18 + Vite + TypeScript UI (auth, movies, train, recs).
- [x] **2.6** Root: `docker-compose.yml` (Postgres 16, API, web), `.env.example`, `.gitignore`.

**You do next**

- [ ] **2.7** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) if not already installed.
- [ ] **2.8** From project root: `docker compose up --build` — wait until API and web are healthy.
- [ ] **2.9** In browser: `http://localhost:5173` — register, log in, rate several movies, click **Train model**, then **Refresh recommendations**.

---

## Phase 3 — Integrate (secrets + cloud DB)

- [ ] **3.1** Create a [Neon](https://neon.tech) project; copy the Postgres connection string.
- [ ] **3.2** Set `DATABASE_URL` for SQLAlchemy using **`postgresql+psycopg://`** (adjust user/host/db/query params as Neon shows).
- [ ] **3.3** Set `BETTER_AUTH_SECRET` to a long random string (used as JWT signing secret in this repo).
- [ ] **3.4** Redeploy or restart API with updated env; run migrations (`alembic upgrade head` inside container or locally against Neon).

Note: wiring the external **Better Auth** hosted product is optional; this codebase uses the same env names for JWT.

---

## Phase 4 — Git + GitHub

- [x] **4.1** `git init` and initial commit (excluding `.env`, `node_modules`, `*.pkl` via `.gitignore`).

**GitHub (linked)**

- [x] **4.2** Remote repo: [Moive-Recommendation-Engine](https://github.com/Saisuman55/Moive-Recommendation-Engine).
- [x] **4.3** `git remote add origin https://github.com/Saisuman55/Moive-Recommendation-Engine.git`
- [x] **4.4** `main` pushed and tracking `origin/main` (merged existing `README.md` from GitHub).

---

## Phase 5 — Quality

**You do next**

- [ ] **5.1** Install [CodeRabbit](https://coderabbit.ai) on the GitHub repository.
- [ ] **5.2** Open a small PR (or push commits) and address automated review comments.

---

## Antigravity-style batch prompt (if you use a task generator)

Paste your three docs, then:

> Based on the uploaded PRD, Design, and Tech Stack docs, generate a proper project todo list for **Movie Recommendation Engine**. Each task should be atomic — one task at a time, sequentially ordered, with no overlapping dependencies.

This file (`TASKS.md`) is the working checklist for this repository.
