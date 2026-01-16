# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LocalHero is a full-stack web application with a Python FastAPI backend and Next.js TypeScript frontend.

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
