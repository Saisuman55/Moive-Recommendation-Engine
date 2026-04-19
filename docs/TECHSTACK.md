# Tech Stack — Movie Recommendation Engine (2026)

## Choices and rationale

| Layer | Choice | Why |
|-------|--------|-----|
| API | **FastAPI** | Async-friendly, automatic OpenAPI, strong typing with Pydantic v2. |
| Auth (app) | **JWT + bcrypt** (secret from `BETTER_AUTH_SECRET`) | Matches panel env var naming; stateless API tokens. Full **Better Auth** SaaS is optional and typically Node-hosted. |
| ORM | **SQLAlchemy 2.x** | Mature relational modeling for `users`, `movies`, `ratings`, `recommendations`. |
| Migrations | **Alembic** | Versioned schema for Postgres (local Docker or Neon). |
| Database | **PostgreSQL 16** (Docker) / **Neon** (serverless) | JSON-friendly ecosystem, stable drivers (`psycopg` v3). |
| ML | **scikit-surprise** — **SVD** | Standard matrix factorization for collaborative filtering class projects. |
| Model artifact | **Pickle** (`.pkl`) on disk volume | Simple reload after train; excluded from Git. |
| Frontend | **React 18** + **TypeScript** + **Vite** | Fast dev server, small config, modern JSX transform. |
| DevOps | **Docker Compose** | One command for DB + API + web for demos. |
| Quality | **CodeRabbit** (GitHub) | Automated PR review — install on the repo when hosted on GitHub. |

## Environment variables

See repository `.env.example`. Minimum:

- `DATABASE_URL` — SQLAlchemy URL, e.g. `postgresql+psycopg://...`
- `BETTER_AUTH_SECRET` — long random string (used as JWT signing secret in this codebase).
- `BETTER_AUTH_URL` — frontend origin (CORS / future deep links).
- `CORS_ORIGINS` — comma-separated allowed browser origins.

## Deployment notes

- API: any container host or PaaS that runs Docker; run `alembic upgrade head` before or on startup.
- DB: Neon connection string with `sslmode=require` in URL query where applicable.
- Frontend: static build (`npm run build`) to CDN/host; set `VITE_API_URL` at build time for production APIs.
