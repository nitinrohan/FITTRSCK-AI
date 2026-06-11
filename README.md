# FitTrack AI

An AI-powered personal fitness tracker for workouts, nutrition, body measurements, wellness, habits, goals, and progress insights.

The MVP is designed for one user and built to expand into a multi-user platform supporting trainers, clients, gyms, organizations, and wearable integrations.

---

## Features (Phase 1 — Foundation)

- Clean project structure with frontend, backend, and infrastructure separation
- FastAPI backend with health + readiness endpoints, structured logging, and OpenAPI docs
- Next.js 14 App Router frontend with TypeScript strict mode and Tailwind CSS
- PostgreSQL with SQLAlchemy 2.0 and Alembic migrations
- Docker Compose for local development
- Environment-based configuration with no hard-coded secrets
- Backend tests with pytest (18 passing), ruff lint (clean), mypy type-checking
- GitHub Actions CI pipeline

---

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop) 4.x+
- [Docker Compose](https://docs.docker.com/compose/) v2.x (included with Docker Desktop)
- (Optional for local dev without Docker) Python 3.11+, Node 20+, PostgreSQL 15

---

## Quick Start

### 1. Clone and configure

```bash
git clone <repo-url> fittrack-ai
cd fittrack-ai
cp .env.example .env
```

Edit `.env` — at minimum change:
- `POSTGRES_PASSWORD`
- `APP_SECRET_KEY`
- `JWT_SECRET_KEY`

### 2. Start all services

```bash
make up
# or: docker-compose up -d
```

This starts:
- **PostgreSQL** on port 5432
- **FastAPI API** on port 8000 (with hot-reload)
- **Next.js Web** on port 3000 (with hot-reload)

Migrations run automatically before the API starts.

### 3. Verify

```
http://localhost:3000     — Web app
http://localhost:8000     — API root
http://localhost:8000/docs — OpenAPI documentation
http://localhost:8000/health — Liveness check
http://localhost:8000/ready  — Readiness check (DB connectivity)
```

---

## Environment Variables

See [`.env.example`](./.env.example) for all available variables with descriptions.

Key variables:

| Variable | Description |
|---|---|
| `DATABASE_URL` | Full PostgreSQL connection string |
| `APP_SECRET_KEY` | Application secret (min 32 chars) |
| `JWT_SECRET_KEY` | JWT signing secret (min 32 chars) |
| `APP_ENV` | `development` \| `production` \| `test` |
| `AI_PROVIDER` | `anthropic` \| `openai` \| `none` |
| `ANTHROPIC_API_KEY` | Anthropic API key (backend-only) |
| `NEXT_PUBLIC_API_URL` | API URL visible to the browser |

---

## Development Commands

All commands are available via `make`. Run `make help` for the full list.

### Database

```bash
make migrate          # Apply pending migrations
make migration m="add users table"  # Generate a new migration
make seed             # Load development seed data
make shell-db         # Open psql session
```

### Testing

```bash
make test-api         # Run backend pytest suite
make test-web         # Run frontend jest suite
make test             # Run both
```

### Linting and type-checking

```bash
make lint-api         # ruff check
make typecheck-api    # mypy
make lint-web         # eslint
make typecheck-web    # tsc --noEmit
make lint             # Both
```

### Logs

```bash
make logs             # All services
make logs-api         # API only
```

---

## Running Without Docker

### Backend

```bash
cd apps/api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Set environment
export DATABASE_URL="postgresql://fittrack:changeme@localhost:5432/fittrack"
export APP_SECRET_KEY="your-secret"
export JWT_SECRET_KEY="your-jwt-secret"

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd apps/web
npm ci

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm run dev   # http://localhost:3000
```

---

## Project Structure

```
fittrack-ai/
├── apps/
│   ├── api/                  # FastAPI backend
│   │   ├── app/
│   │   │   ├── main.py       # App factory, middleware, router wiring
│   │   │   ├── config.py     # Settings (pydantic-settings)
│   │   │   ├── database.py   # SQLAlchemy engine and session
│   │   │   ├── logging_config.py
│   │   │   ├── exceptions.py # Custom exceptions + handlers
│   │   │   ├── models/       # SQLAlchemy ORM models
│   │   │   ├── schemas/      # Pydantic request/response schemas
│   │   │   ├── routers/      # FastAPI route handlers
│   │   │   └── core/         # Shared utilities (pagination etc.)
│   │   ├── alembic/          # Database migrations
│   │   └── tests/            # pytest test suite
│   └── web/                  # Next.js 14 frontend
│       └── src/
│           ├── app/          # App Router pages and layouts
│           ├── components/   # Reusable UI components
│           └── lib/          # API client, utilities, types
├── docs/                     # Architecture and design documentation
├── .github/workflows/        # GitHub Actions CI
├── docker-compose.yml
├── .env.example
└── Makefile
```

---

## Running Tests Manually

### Backend (all 18 passing)

```bash
cd apps/api
export APP_ENV=test
export DATABASE_URL="postgresql://fittrack:testpassword@localhost:5432/fittrack_test"
export APP_SECRET_KEY="test-secret"
export JWT_SECRET_KEY="test-jwt-secret"
pytest tests/ -v
```

### Lint

```bash
cd apps/api
ruff check app tests   # Should report: All checks passed!
```

---

## Troubleshooting

**`make up` fails with DB connection error**
The API retries until the DB health check passes. Wait 10–15 seconds and check `make logs-api`.

**Port already in use**
Change the host port in `docker-compose.yml` (e.g. `"8001:8000"` for the API).

**Migrations fail**
Run `make shell-api` then `alembic history` to see the current state. Check `make logs-api` for the error detail.

**Hot-reload not working**
Ensure the source volumes are mounted (check `docker-compose.yml`). Restart with `make down && make up`.

---

## Documentation

- [`docs/architecture.md`](./docs/architecture.md) — System design and component overview
- [`docs/decision-log.md`](./docs/decision-log.md) — Architecture decision records
- [`docs/data-model.md`](./docs/data-model.md) — Database schema (Phase 2+)
- [`docs/api.md`](./docs/api.md) — API reference (Phase 2+)
- [`docs/security.md`](./docs/security.md) — Security design (Phase 2+)
- [`docs/ai-design.md`](./docs/ai-design.md) — AI assistant architecture (Phase 6+)

---

## Implementation Phases

| Phase | Focus | Status |
|---|---|---|
| 0 | Workspace audit | ✅ Complete |
| 1 | Foundation | ✅ Complete |
| 2 | Authentication and user profiles | ✅ Complete |
| 3 | Exercise library | ✅ Complete |
| 4 | Workout templates | 🔜 Next |
| 5 | Workout logging and history | Planned |
| 6 | Nutrition and wellness | Planned |
| 7 | Measurements, goals, dashboard | Planned |
| 8 | AI assistant | Planned |
| 9 | Privacy, export, polish | Planned |
