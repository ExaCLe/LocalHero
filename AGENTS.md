# Project Context

**Stack:** Next.js (Frontend), FastAPI (Backend), PostgreSQL (Database).
**Deployment:** Vercel (Frontend), Vercel/Railway/AWS (Backend).
**Architecture:** Hybrid Rendering. The Next.js App Router handles Server-Side Rendering (SSR) and Server Components (
RSC), interacting with the FastAPI backend via REST.

---

# 1. Naming Conventions (STRICT)

**Goal:** clarity over brevity. Code must be self-documenting.

* **Be Descriptive:** Name variables for what they *are*.
    * ❌ `i`, `res`, `data`, `val`
    * ✅ `row_index`, `api_response`, `user_profile`, `transaction_value`
    * **Do not abbreviate.** (e.g., use `calculate_total`, not `calc_tot`).
* **Include Units:** Numeric variables must include their unit in the suffix.
    * ✅ `timeout_seconds`, `sampling_rate_hz`, `file_size_bytes`, `price_usd`.
* **No Hungarian Notation:** Do not prefix names with type information.
    * ❌ `str_name`, `list_users`, `dict_config`
    * ✅ `name`, `users`, `config`
* **No "Utils" Dumps:** Generic file names are forbidden. Group code by domain/purpose.
    * ❌ `utils.py`, `helpers.py`, `common.py`
    * ✅ `data_normalization.py`, `date_formatting.py`, `jwt_handler.py`
* **Casing Styles:**
    * **Python:** `snake_case` for variables/functions/modules. `PascalCase` for Classes/Pydantic Models.
    * **TypeScript/JS:** `camelCase` for variables/functions. `PascalCase` for Components/Classes. `kebab-case` for
      filenames, routes and folders: `lowercase`.
* **Consistency:** If a concept is named `user_id` in the database, do not call it `uid` in the frontend. Maintain
  terminology across the stack.

---

# 2. Code Documentation & Comments

* **Self-Documenting Code:** The strict naming conventions above are the primary form of documentation.
* **The "No-What" Rule:** Never write a comment explaining *what* the code is doing. If the code is hard to read,
  refactor it, rename variables, or extract functions.
* **The "Why" Exception:** Comments are permitted **only** to explain the reasoning behind unconventional decisions,
  specific business logic constraints, or workarounds for external library bugs.
    * ❌ `# Loop through users and save to DB`
    * ✅ `# We use a bulk insert here instead of ORM save() to reduce round-trips for datasets > 10k rows.`

---

# 3. Testing Strategy: High Value, Low Boilerplate

**Goal:** Confidence in deployment with minimal maintenance cost. Avoid "testing implementation details."

* **Prioritize Integration Tests:** Focus on "Vertical Slices." Test that an endpoint accepts data, persists it to the
  DB, and returns the correct response.
* **Avoid Excessive Mocking:** Do not mock the database or internal service calls unless absolutely necessary (e.g.,
  external 3rd party APIs like Stripe/SendGrid). Use a real test database (containerized via Docker).
* **Efficient Coverage:**
    * Write one comprehensive test case covering the "happy path" and the most critical "edge case."
    * Avoid writing 10 separate unit tests for helper functions if they are covered by the main integration test.
* **Tooling:**
    * **Backend:** `pytest` with `TestClient` (FastAPI) and `testcontainers` (for real Postgres instances).
    * **Frontend:** Playwright/Cypress for E2E flows. Avoid heavy Jest unit testing for UI components unless they
      contain complex logic.

---

# 4. Architecture & Coding Best Practices

### Backend (FastAPI)

* **Pydantic Everything:** Use Pydantic models for all Request bodies, Response schemas, and Environment variable
  validation.
* **Dependency Injection:** Use FastAPI `Depends` for database sessions and authentication dependencies.
* **SQLAlchemy**: Prefer the synchronous engine unless performance requires async.
* **Migrations:** All database changes must be done via `alembic`. Never alter the DB manually.

## Frontend (Next.js)

* **Server Components (RSC):** Fetch data in Server Components whenever possible to reduce client-side waterfalls.
* **Type Safety:** Generate TypeScript interfaces from the FastAPI OpenAPI `json` schema (using tools like
  `openapi-typescript-codegen`) to ensure frontend/backend contract alignment.

---

# 5. Workflow & Quality Assurance

* **Linting:**
    * **Linting**: ruff for lint-only, black for formatting.
    * **TypeScript:** Use `ESLint`.
* **Pre-commit Hooks:** Ensure `ruff check`, `ruff format`, and `tsc --noEmit` run before every commit.
* **CI/CD:** Pipelines must fail if the linter warns or integration tests fail.
