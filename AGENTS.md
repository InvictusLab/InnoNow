# Repository Guidelines

## Project structure

- `backend/app/` contains the FastAPI service. Add endpoints in `api/routes/`, SQLModel definitions in `models.py`, and database operations in `crud.py`. Commit schema migrations under `alembic/versions/`.

- `frontend/src/` contains the React and TypeScript application. Put pages in `routes/`, shared components in `components/`, and static images in `frontend/public/assets/images/`.

- Edit email templates in `packages/react-email/emails/` and run `bun run email:export` from the repository root to update the backend HTML.

## Local development and builds

1. From the root, run `docker compose up -d --wait db mailpit` to start PostgreSQL and the local email catcher.

2. From `backend/`, run `uv sync`, then `uv run bash scripts/prestart.sh` to apply migrations and create the initial user. Start the API with `uv run fastapi dev` on port 8000.

3. In another terminal at the root, run `bun install`, then `bun run dev` to start Vite on port 5173.

Run `bun run build` from `frontend/` to type-check and build the UI into `backend/app/frontend/`.

After changing the API schema, run `bash scripts/generate-client.sh` from the root to refresh `frontend/src/client/`.

## Coding style and naming

Use four spaces and `snake_case` for Python functions. Ruff formats Python and sorts imports.

Use two spaces and double quotes in TypeScript. Name React components in PascalCase and hooks in camelCase with a `use` prefix, as in `useAuth`.

Run `uv run prek run --all-files` from the root for Biome, Ruff, and type checks.

## Testing

- Place pytest cases in `backend/tests/` as `test_*.py`. Use a disposable database because teardown deletes users and items. From `backend/`, run `uv run bash scripts/test.sh` to run pytest and generate `htmlcov/index.html`. CI requires at least 90% backend coverage.

- Place Playwright browser tests in `frontend/tests/` as `*.spec.ts`. With the development API and Mailpit running, run `bun run test` from the root. Playwright starts or reuses Vite.

## Commits and pull requests

Write short, imperative commit subjects. History includes `feat(innonow): initialize the project`.
