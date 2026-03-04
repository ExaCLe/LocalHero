# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LocalHero is a full-stack web application using a Convex backend and a Next.js TypeScript frontend.
The frontend uses Next.js App Router (SSR/RSC) and can call Convex functions directly.

## Commands

### Convex Backend (from `frontend/` directory)

```bash
npm run convex:dev       # Start Convex dev workflow (configures + deploys dev functions)
npm run convex:dev:once  # One-time Convex push/codegen step
npm run convex:codegen   # Regenerate Convex generated types (requires configured deployment)
```

### Frontend (from `frontend/` directory)

```bash
npm run dev          # Start dev server (http://localhost:3000)
npm run build        # Production build
npm run lint         # ESLint
npm run type-check   # TypeScript check
npm test             # Playwright tests
npm test -- path/to/spec.ts  # Run a single Playwright spec
```

### Pre-commit (from root)

```bash
pre-commit run --all-files  # Run frontend lint + type-check hooks
```

## Architecture

```
LocalHero/
├── frontend/               # Next.js 16 + React 19 + TypeScript + Convex
│   ├── app/                # Next.js App Router pages
│   ├── convex/             # Convex functions and schema
│   ├── components/         # Shared React components
│   └── tests/              # Playwright E2E tests
├── .github/workflows/      # CI (frontend + pre-commit)
└── .pre-commit-config.yaml
```

## Environment Setup

**Frontend `frontend/.env.local`:**

```bash
NEXT_PUBLIC_CONVEX_URL=<your-convex-deployment-url>
```

Optional for Convex CLI / self-hosted Convex (Convex OSS) setups:

```bash
CONVEX_DEPLOYMENT=<deployment-name>
CONVEX_SELF_HOSTED_URL=<self-hosted-convex-url>
```

## Key Configuration

- **TypeScript:** Strict mode, ES2017 target (Next.js app) + Convex TS config in `frontend/convex/tsconfig.json`
- **Backend Runtime:** Convex functions (`frontend/convex/*`)
- **CI:** Runs pre-commit and frontend Playwright tests

## Coding Standards

### Naming Conventions

- **Be descriptive, no abbreviations:** `user_profile` not `data`, `calculate_total` not `calc_tot`
- **Include units in numeric variables:** `timeout_seconds`, `file_size_bytes`, `price_usd`
- **No Hungarian notation:** `users` not `list_users`
- **No generic filenames:** Use `date-formatting.ts` not `utils.ts` or `helpers.ts`
- **Casing:**
    - TypeScript: `camelCase` for variables/functions, `PascalCase` for components, `kebab-case` for filenames
    - Convex function exports: descriptive names (`status`, `createUser`, `listUsers`)
- **Consistency across stack:** Keep naming consistent between frontend code, Convex schema, and function args

### Comments

- **No "what" comments** - refactor unclear code instead
- **Only "why" comments** - explain unconventional decisions, business logic constraints, or workarounds

### Testing

- **Prioritize integration/E2E tests** over isolated component tests when validating user flows
- **Avoid excessive mocking** - prefer real page interactions in Playwright
- **Frontend:** Playwright for E2E; keep UI smoke tests focused and reliable
- **Convex:** Test through user-visible flows or server-side integration points when possible

### Backend Patterns (Convex)

- Put backend functions in `frontend/convex/`
- Use Convex queries/mutations/actions for backend logic instead of custom FastAPI routes
- Keep schemas in `frontend/convex/schema.ts`
- Prefer typed Convex function references when codegen is available; use generic builders only when bootstrapping/migrating

### Frontend Patterns

- Fetch data in Server Components when practical to reduce client waterfalls
- Keep auth pages and forms simple unless a design system is established
- Use `NEXT_PUBLIC_CONVEX_URL` for Convex client configuration
