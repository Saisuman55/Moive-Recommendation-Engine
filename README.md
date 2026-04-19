# Moive-Recommendation-Engine

Movie recommendation engine: **FastAPI** API, **React 18** (Vite) UI, **Surprise SVD** model, **PostgreSQL** (Docker or Neon) or **SQLite** for quick local runs, **Alembic** migrations (Postgres).

## Why localhost might not run

1. **Docker not installed** — On this machine `docker` was not on `PATH`. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and restart the terminal, *or* use the **no-Docker** steps below.
2. **Python is the Microsoft Store stub** — If `python` opens the Store, install **Python 3.11+** from [python.org](https://www.python.org/downloads/) and tick **“Add python.exe to PATH”**.
3. **Postgres not running** — The old default expected Postgres on `localhost:5432`. The API now **defaults to SQLite** so the backend can start without Postgres unless you set `DATABASE_URL` to Postgres.

## Quick start (no Docker) — Windows

From the repo root in PowerShell:

```powershell
.\start-dev.ps1
```

Then open **http://127.0.0.1:5173** (API docs: **http://127.0.0.1:8000/docs**).

The script creates `backend\venv`, installs dependencies once, runs the API with **SQLite** (`backend\movie_rec.db`), and starts Vite. In **development**, the UI calls **`/api/...`** on the same host as Vite; Vite **proxies** that to `http://127.0.0.1:8000`, which avoids CORS and “Failed to fetch” when the page is opened as `localhost` vs `127.0.0.1`.

**Backend only**

```powershell
.\backend\start.ps1
```

Opens **http://127.0.0.1:8000/docs** (uses `backend\.env` and SQLite by default).

**Manual equivalent**

```powershell
cd backend
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
$env:DATABASE_URL="sqlite:///./movie_rec.db"
.\venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

New terminal:

```powershell
cd frontend
npm install
$env:VITE_API_URL="http://127.0.0.1:8000"
npm run dev -- --host 127.0.0.1 --port 5173
```

## Quick start (Docker)

1. Install Docker Desktop and ensure `docker compose version` works in a **new** terminal.
2. Copy `.env.example` to `backend/.env` if you want overrides.
3. From the repo root: `docker compose up --build`
4. Open **http://localhost:5173** (API: **http://localhost:8000/docs**).

## Docs

- [docs/PRD.md](docs/PRD.md) — product requirements  
- [docs/DESIGN.md](docs/DESIGN.md) — UI design notes  
- [docs/TECHSTACK.md](docs/TECHSTACK.md) — stack and env vars  
- [docs/TASKS.md](docs/TASKS.md) — checklist (Neon, CodeRabbit, etc.)

Remote: [github.com/Saisuman55/Moive-Recommendation-Engine](https://github.com/Saisuman55/Moive-Recommendation-Engine).
