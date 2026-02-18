# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LocalHero is a full-stack web application with a Python FastAPI backend and Next.js TypeScript frontend. Uses hybrid
rendering with Next.js App Router (SSR/RSC) communicating with FastAPI via REST.

## Commands

### Backend (from `backend/` directory)

```bash
uvicorn main:app --reload              # Start dev server (http://localhost:8000)
pytest -q --maxfail=1 --cov=.          # Run tests with coverage
alembic upgrade head                   # Apply all migrations
alembic revision --autogenerate -m "message"  # Create new migration
```

### Frontend (from `frontend/` directory)

```bash
npm run dev          # Start dev server (http://localhost:3000)
npm run build        # Production build
npm run lint         # ESLint
npm run type-check   # TypeScript check
npm test             # Jest tests
npm test -- path/to/test.tsx  # Run single test file
```

### Pre-commit (from root)

```bash
pre-commit run --all-files  # Run all hooks (ruff, black, mypy, eslint, type-check)
```

## Architecture

```
LocalHero/
├── backend/           # FastAPI + SQLAlchemy + PostgreSQL
│   ├── app/
│   │   ├── main.py        # FastAPI app entry, routes
│   │   ├── database.py    # DB connection & session
│   │   ├── models.py      # SQLAlchemy ORM models
│   │   ├── schemas.py     # Pydantic request/response schemas
│   │   └── crud.py        # Database operations
│   ├── alembic/           # Migration scripts
│   └── tests/             # pytest tests
├── frontend/          # Next.js 16 + React 19 + TypeScript
│   ├── app/               # Next.js App Router pages
│   ├── components/        # React components
│   └── __tests__/         # Jest + React Testing Library
└── .pre-commit-config.yaml
```

## Environment Setup

**Backend `.env`:**

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/local_hero
```

**Frontend `.env.local`:**

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Key Configuration

- **Python:** 3.11+, Black (88 chars), Ruff (140 chars), MyPy strict mode
- **TypeScript:** Strict mode, ES2017 target
- **Database:** PostgreSQL 15
- **CI:** Runs lint, backend tests, and frontend tests in parallel

## Coding Standards

### Naming Conventions

- **Be descriptive, no abbreviations:** `user_profile` not `data`, `calculate_total` not `calc_tot`
- **Include units in numeric variables:** `timeout_seconds`, `file_size_bytes`, `price_usd`
- **No Hungarian notation:** `users` not `list_users`
- **No generic filenames:** Use `date_formatting.py` not `utils.py` or `helpers.py`
- **Casing:**
    - Python: `snake_case` for variables/functions, `PascalCase` for classes/Pydantic models
    - TypeScript: `camelCase` for variables/functions, `PascalCase` for components, `kebab-case` for filenames
- **Consistency across stack:** If it's `user_id` in the database, don't call it `uid` in frontend

### Comments

- **No "what" comments** - refactor unclear code instead
- **Only "why" comments** - explain unconventional decisions, business logic constraints, or workarounds
- **No redundant docstrings** - avoid docstrings that simply restate the function name or describe what is obvious from the code (e.g., `"""Get a user by email."""` for a function named `get_user_by_email`)
- **No inline comments describing obvious operations** - avoid comments like `# Validate email uniqueness` before `if get_user_by_email(db, email):`
- **No numbered flow comments** - avoid docstrings that list steps like "1. Do X, 2. Do Y" - the code should be self-explanatory

### Testing

- **Prioritize integration tests** over unit tests - test vertical slices (endpoint → DB → response)
- **Avoid excessive mocking** - use real test database, only mock external APIs (Stripe, SendGrid)
- **Backend:** pytest with TestClient
- **Frontend:** Playwright/Cypress for E2E; avoid heavy Jest unit testing for simple UI components

### Backend Patterns

- Use Pydantic models for all requests, responses, and environment validation
- Use FastAPI `Depends` for DB sessions and auth
- Prefer synchronous SQLAlchemy unless performance requires async
- All DB changes via Alembic migrations only

### Frontend Patterns

- Fetch data in Server Components to reduce client-side waterfalls
- Generate TypeScript interfaces from FastAPI OpenAPI schema for type safety
